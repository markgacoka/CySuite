import re
import io
import subprocess
import puremagic
import urllib
import hashlib
import urllib.parse
from os import path
from .tasks import scan_subdomains
import os, json, base64, requests
from html import escape, unescape
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TransactionForm
from .forms import ProjectForm
from .forms import WordlistForm
from .models import PayloadModel
from .models import WordlistModel
from .models import ProjectModel
from .models import SubdomainModel
from cyauth.models import Account
from PIL import Image
from django.template.context_processors import csrf
from django.conf import settings
from django.contrib import messages
from django.core.files import File
from django.http import FileResponse
from django.core.files.storage import default_storage
from scripts.WordlistGen.wordlist import print_wordlist
from scripts.WordlistGen.status import url_status
from scripts.Headers.request import send_request
from scripts.Hashes.hashid import HashID
from scripts.IPAddress.get_ip import get_client_ip
from scripts.HexViewer.hexviewer import hex_viewer
from scripts.CodeInjection.injector import Injector
from scripts.HexViewer.full_hexviewer import full_hex_viewer
from scripts.WordlistGen.generator import extract_wordlist


def checkout(request):
    return render(request, 'pages/checkout.html', context={
        'PAYPAL_CLIENT_ID': os.environ.get('PAYPAL_CLIENT_ID'),
    })

def update_transaction(request):
    if request.method == 'POST':
        context['profile_account'] = request.user.profile
        resp_obj = json.loads(request.body)
        unclean_res = {
            "user_account": request.user.username if request.user.is_authenticated else 'None',
            "given_name": resp_obj['payer']['name']['given_name'],
            "last_name": resp_obj['payer']['name']['surname'],
            "payer_email": resp_obj['payer']['email_address'],
            "amount": float(resp_obj['purchase_units'][0]['payments']['captures'][0]['amount']['value']),
            "currency": resp_obj['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code'],
            "status": resp_obj['status'],
            "transaction_code": resp_obj['id']
        }

        transaction_form = TransactionForm(unclean_res)
        if transaction_form.is_valid():
            transaction_form.save()
            message = 'Transaction completed successfully!'
        else:
            message = 'A server side error occurred!'
    else:
        message = 'An error occurred!'
    return HttpResponse(message)

def privacy_policy(request):
    return render(request, 'pages/privacy-policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms-conditions.html')

def projects(request):
    context = {}
    projects = ProjectModel.objects.filter(project_user=request.user)
    project_list = []
    for project in projects:
        project_details = {}
        project_model_output = project.get_project_details()
        project_details['project'] = project_details.get('project', project_model_output[0])
        project_details['program'] = project_details.get('program', project_model_output[1])
        project_details['progress'] = project_details.get('progress', project_model_output[2])
        project_list.append(project_details)

    if request.method == 'POST':
        if 'delete-project' in request.POST.keys():
            try:
                ProjectModel.objects.filter(project_name__iexact=request.POST.get('delete-project')).filter(project_user=request.user).delete()
                messages.success(request, 'Project has been deleted successfully!')
                return redirect('projects')
            except:
                context['error_message'] = 'An error occurred!'
                return redirect('projects')
        elif 'view' in request.POST.keys():
            try:
                curr_project = request.POST.get('view')
                request.session['project'] = curr_project
                request.session.modified = True
                response = {'status': 1, 'message': "Ok"}
            except:
                response = {'status': 0, 'message': "Something went wrong!"}
            return HttpResponse(json.dumps(response), content_type='application/json')
        elif ('in_scope_domains' and 'project_name' and 'program') in request.POST.keys():
            tempdict = request.POST.copy()
            tempdict['in_scope_domains'] = tempdict['in_scope_domains'].split('\r\n')
            request.POST = tempdict
            context['profile_account'] = request.user.profile
            if ProjectModel.objects.filter(project_user=request.user).filter(project_name__iexact=request.POST.get('project_name')).exists():
                context['project_list'] = project_list
                context['error_message'] = 'Project name already exists!'
            else:
                project_form = ProjectForm(request.POST)
                if project_form.is_valid():
                    project_model = ProjectModel.objects.create(
                        project_name = project_form.cleaned_data['project_name'],
                        program = project_form.cleaned_data['program'],
                        in_scope_domains = [],
                        progress = 0,
                        subdomains = [],
                        project_user = request.user)

                    for domain in project_form.cleaned_data['in_scope_domains']:
                        if domain != None and domain != '':
                            project_model.in_scope_domains.append(domain.strip())
                    project_model.save()

                    request.session['project'] =  project_form.cleaned_data['project_name']
                    request.session.modified = True
                    messages.success(request, 'Project has been created successfully!')
                    return redirect('projects')
                else:
                    context['error_message'] = 'An error occurred!'
                    context['project_list'] = project_list
        else:
            context['project_list'] = project_list
        context['profile_account'] = request.user.profile
    else:
        context['project_list'] = project_list
        context['project_details'] = project_list
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/projects.html', context)

def notes(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/notes.html', context)

def subdomain_enum(request):
    context = {}
    info_list = []
    project_session = request.session['project']
    project_model_instance = ProjectModel.objects.filter(project_user=request.user).filter(project_name__iexact=project_session)

    if request.method == 'POST':
        if 'scan' in request.POST.keys():
            user_id = Account.objects.filter(username=request.user.username).values('user_id')[0]['user_id']
            task = scan_subdomains.delay(user_id, project_session)
            context['task'] = task
            context['task_id'] = task.task_id
            context['profile_account'] = request.user.profile
            messages.success(request, 'Scan in progress. Stand by!')
        return render(request, 'dashboard/subdomain_enum.html', context)
    else:
        if len(project_model_instance.values_list()) > 0:
            context['is_project'] = 'True'
            if project_model_instance.count() > 0:
                scan = project_model_instance.values('subdomains')
                if len(scan[0]['subdomains']) > 0:
                    context['first_scan'] = 'False'
                else:
                    context['first_scan'] = 'True'
            else:
                context['first_scan'] = 'True'
        else:
            context['is_project'] = 'False'
            context['profile_account'] = request.user.profile
            return render(request, 'dashboard/subdomain_enum.html', context)

        user_projects = ProjectModel.objects.get(project_name=request.session['project'])
        subdomain_model_instance = SubdomainModel.objects.filter(subdomain_user=request.user).filter(project=user_projects)
        for model in subdomain_model_instance.values_list():
            subdomain_info = {}
            subdomain_info['subdomain'] = model[3]
            subdomain_info['status_code'] = model[4]
            subdomain_info['screenshot'] = model[5]
            subdomain_info['ip_address'] = model[6]
            subdomain_info['waf'] = model[7]
            subdomain_info['ssl_info'] = model[8]
            subdomain_info['header_info'] = model[9]
            info_list.append(subdomain_info)
    context['subdomain_info'] = info_list
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/subdomain_enum.html', context)


def directory_enum(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/directory_enum.html', context)

def vuln_analysis(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/vuln_analysis.html', context)
    
def dorking(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/dorking.html', context)

def exploit(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/exploits.html', context)

def req_tamperer(request):
    context = {}
    if request.method == 'POST':
        if request.POST['req_url'] == '' or request.POST['req_url'] == None:
            pass
        else:
            url = request.POST.get('req_url')
            method = request.POST.get('req-method')
            data = [request.POST.get('data-key'), request.POST.get('data-value')]
            auth = [request.POST.get('user'), request.POST.get('pass')]
            header = [request.POST.get('header-name'), request.POST.get('header-value')]
            if (request.POST.get('req-method') == 'GET' or request.POST.get('req-method') == 'HEAD') and (request.POST.get('data-key') != '' and request.POST.get('data-key') != ''):
                context['error_message'] = '[GET/HEAD] The data is already passed through the query string.'
                context['profile_account'] = request.user.profile
                return render(request, 'dashboard/req_tamperer.html', context)
            req_header, resp_header = send_request(request, url, method, data, auth, header)
            if req_header == None and resp_header == None:
                context['error_message'] = 'Invalid URL format.'
                context['profile_account'] = request.user.profile
                return render(request, 'dashboard/req_tamperer.html', context)
            context['request_output'] = req_header
            context['response_output'] = resp_header
            context['profile_account'] = request.user.profile
    else:
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/req_tamperer.html', context)

def wordlist_gen(request):
    context = {}
    if request.method == 'POST':
        names = WordlistModel.objects.get(wordlist_user=request.user)
        wordlist_values = names.return_db_values()
        isNone = all(v.name is None for v in wordlist_values)
        wordlist_result = {}
        if isNone:
            context['wordlist_list'] = ''
        else:
            for i in wordlist_values:
                if i.name is not None and i.name != '':
                    wordlist_result[i.name.split('/')[-1]] = wordlist_result.get(i.url, i.url)
        context['wordlist_list'] = wordlist_result

        if 'preview' in request.POST.keys():
            context['preview_wordlist'] = next(print_wordlist(request.POST.get('preview')[1:], 20))
            context['url_status'] = 'N/A'
            context['wordlist_len'] = 0
            context['wordlist_output'] = ''
            context['profile_account'] = request.user.profile
        elif 'wordlist' in request.FILES.keys():
            wordlist_form = WordlistForm(request.POST, request.FILES, instance=request.user)
            current_user = WordlistModel.objects.get(wordlist_user=request.user)
            current_object = WordlistModel.objects
            file_data = request.FILES['wordlist']
            file_dir = 'wordlists/{}/'.format(request.user.user_id)
            filename = file_dir + file_data.name

            if os.path.isfile('media/' + filename):
                messages.success(request,"Filename already in use. Please rename your file.")
                return redirect('wordlist_gen')

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            new_dir = BASE_DIR + '/media' + '/wordlists/{}/'.format(request.user.user_id)
            if not os.path.isdir(new_dir):
                os.mkdir(new_dir)

            with open('media/' + filename, 'wb') as file_a:
                file_a.write(file_data.read())
            if wordlist_form.is_valid():
                if not current_user.wordlist_file_3:
                    current_object.filter(wordlist_user=request.user).update(wordlist_file_3=filename)
                    messages.success(request,"The wordlist file has been uploaded successfully!")
                elif not current_user.wordlist_file_4:
                    current_object.filter(wordlist_user=request.user).update(wordlist_file_4=filename)
                    messages.success(request,"The wordlist file has been uploaded successfully!")
                elif not current_user.wordlist_file_5:
                    current_object.filter(wordlist_user=request.user).update(wordlist_file_5=filename)
                    messages.success(request,"The wordlist file has been uploaded successfully!")
                else:
                    messages.success(request,'The number of allowed uploads has been exceeded')
                wordlist_form.save()
            return redirect('wordlist_gen')
        elif 'wordlist_url' in request.POST.keys():
            if request.POST['wordlist_url'] == '' or request.POST['wordlist_url'] == None:
                context['wordlist_list'] = wordlist_result
                context['url_status'] = 'N/A'
                context['wordlist_len'] = 0
                context['wordlist_output'] = ''
                context['profile_account'] = request.user.profile
            else:
                wordlist_url = request.POST.get('wordlist_url')
                wordlist = next(extract_wordlist(wordlist_url))
                length = len(wordlist)
                status = url_status(wordlist_url)
                context['url_status'] = status
                context['wordlist_len'] = length
                context['wordlist_output'] = wordlist
                context['profile_account'] = request.user.profile
        elif 'download' in request.POST.keys():
            buffer = io.StringIO()
            wordlist_file = File(buffer, 'w')
            wordlist = request.POST.get('download')
            for word in wordlist.split(','):
                wordlist_file.write(word.replace("{", "").replace("}", "").replace("'", "").replace(" ", "") + '\n')
            response = HttpResponse(buffer.getvalue(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=filename.txt'
            return response
        elif 'preview_new' in request.POST.keys():
            queryset = WordlistModel.objects.get(wordlist_user=request.user)
            url = queryset.return_db_values()[int(request.POST.get('preview_new'))-1]
            return HttpResponse(next(print_wordlist(url.url[1:], 20)))
        elif 'new_delete' in request.POST.keys():
            queryset = WordlistModel.objects.get(wordlist_user=request.user)
            queryset.return_db_values()[int(request.POST.get('new_delete'))-1].delete()
            context['preview_wordlist'] = ''
            context['url_status'] = 'N/A'
            context['wordlist_len'] = 0
            context['wordlist_output'] = ''
            context['success_message'] = 'The file has been deleted successfully!'
            messages.success(request, 'The file has been deleted successfully!')
            context.update(csrf(request))
            return HttpResponse(request)
        else:
            context['url_status'] = 'N/A'
            context['wordlist_len'] = 0
            context['wordlist_output'] = ''
            context['profile_account'] = request.user.profile
    else:
        names = WordlistModel.objects.get(wordlist_user=request.user)
        wordlist_values = names.return_db_values()
        isNone = all(v.name is None for v in wordlist_values)
        wordlist_result = {}
        if isNone:
            context['wordlist_list'] = ''
        else:
            for i in wordlist_values:
                if i.name is not None and i.name != '':
                    wordlist_result[i.name.split('/')[-1]] = wordlist_result.get(i.url, i.url)
            context['wordlist_list'] = wordlist_result
        context['wordlist_len'] = 0
        context['wordlist_output'] = ''
        context['url_status'] = 'N/A'
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/wordlist_gen.html', context)

def decoder(request):
    context = {}
    if request.method == 'POST':
        context['profile_account'] = request.user.profile
        if 'decode' in request.POST:
            input_str = str(request.POST.get('decode-string'))
            if request.POST.get('decoder') == 'None':
                context['decode_output'] = input_str
            elif request.POST.get('decoder') == 'Base64':
                decoded_str = base64.b64decode(input_str).decode('utf-8')
                context['decode_output'] = decoded_str
            elif request.POST.get('decoder') == 'HTML':
                decoded_str = unescape(input_str)
                context['decode_output'] = decoded_str
            elif request.POST.get('decoder') == 'Hex':
                decoded_str = bytes.fromhex(input_str).decode('utf-8')
                context['decode_output'] = decoded_str
            elif request.POST.get('decoder') == 'URL':
                decoded_str = urllib.parse.unquote_plus(input_str)
                context['decode_output'] = decoded_str
            else:
                context['decode_output'] = input_str
            context['encode_output'] = str(request.POST.get('encode-string'))
        elif 'encode' in request.POST:
            input_str = str(request.POST.get('encode-string'))
            if request.POST.get('encoder') == 'None':
                context['encode_output'] = input_str
            elif request.POST.get('encoder') == 'Base64':
                encoded_str = base64.b64encode(input_str.encode('utf-8')).decode('utf-8')
                context['encode_output'] = encoded_str
            elif request.POST.get('encoder') == 'HTML':
                encoded_str = escape(input_str)
                context['encode_output'] = encoded_str
            elif request.POST.get('encoder') == 'Hex':
                encoded_str = input_str.encode("utf-8").hex()
                context['encode_output'] = encoded_str
            elif request.POST.get('encoder') == 'URL':
                encoded_str = urllib.parse.quote_plus(input_str)
                context['encode_output'] = encoded_str
            else:
                context['encode_output'] = input_str
            context['decode_output'] = str(request.POST.get('decode-string'))
        elif 'clear-encoder' in request.POST:
            context['encode_output'] = ''
            context['decode_output'] = str(request.POST.get('decode-string'))
        elif 'clear-decoder' in request.POST:
            context['decode_output'] = ''
            context['encode_output'] = str(request.POST.get('encode-string'))
        elif 'hash' in request.POST.keys():
            hash_str = str(request.POST.get('hash'))
            hash_inst = HashID(hash_str).get_hash()

            if hash_inst:
                result = "[ ", hash_inst[0], " ]"
                return HttpResponse(result)
            else:
                result = 'Could not identify hash type'
                return HttpResponse(result)
        else:
            pass
    else:
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/decoder.html', context)

def injector(request):
    context = {}
    ip_address = get_client_ip(request)

    if request.method == "POST":
        payload = request.POST.get('payload').encode() if request.POST.get('payload') != None else None
        width = int(request.POST.get('width')) if request.POST.get('width') != '' and request.POST.get('width') != None else 0
        height = int(request.POST.get('height')) if request.POST.get('height') != '' and request.POST.get('width') != None else 0
        file_type = request.POST.get('file_type') if request.POST.get('file_type') != None else None
        
        if 'full_hex' in request.POST.keys():
            payload_file = PayloadModel.objects.get(payload_user=request.user)
            filename = payload_file.payload_image.path
            if path.exists(filename):
                img = Image.open(filename)
                width, height = img.size
                hex_dump = next(full_hex_viewer(filename))
                context['hex_dump'] = hex_dump
                context['ipaddress'] = ip_address
                context['profile_account'] = request.user.profile
                context['dimensions'] = (width, height)
                context['file_type'] = puremagic.magic_file(filename)[0].name 
                context['file_size'] = str(os.path.getsize(filename)) + ' bytes'
                context['filename'] = re.sub(r'^.*?/', '', payload_file.payload_image.path)
                context['extension'] = puremagic.magic_file(filename)[0].extension
                context['mime_type'] = puremagic.magic_file(filename)[0].mime_type
                context['byte_match'] = puremagic.magic_file(filename)[0].byte_match.decode('UTF-8','ignore').strip()
                context['download'] = PayloadModel.objects.get(payload_user=request.user).payload_image
                context['status'] = 'Viewing full hex code'
                context.update(csrf(request))
                return render(request, 'dashboard/injector.html', context)
        elif request.POST.get('filename') == '' or '.' not in request.POST.get('filename') or request.POST.get('filename') == None:
            context['status'] = 'Not injected'
            context['error_message'] = 'Filename does not follow the correct filename pattern'
            filename, dimensions = None, (None, None)
        elif type(width) != int or type(height) != int or width < 0 or height < 0:
            context['status'] = 'Not injected'
            context['error_message'] = 'Dimension value should be an integer!'
            filename, dimensions = None, (None, None)
        else:
            filename = 'media/payloads/' + request.POST.get('filename')
            injection = Injector(file_type, width, height, payload, filename)
            filename, dimensions = injection.main()


        if filename != None and dimensions != None:
            new_filename = re.sub(r'^.*?/', '', filename)
            payload_file = PayloadModel.objects.get(payload_user=request.user)
            if new_filename != payload_file.payload_image and payload_file.payload_image != 'default.png':
                try:
                    os.remove(payload_file.payload_image.path)
                except:
                    print("Tried to remove a non-existent payload image")
            payload_file.payload_image = new_filename
            payload_file.save()

            final_filename = re.sub(r'^.*?/', '', new_filename)
            hex_dump = hex_viewer(filename)
            context['hex_dump'] = hex_dump
            context['ipaddress'] = ip_address
            context['profile_account'] = request.user.profile
            context['dimensions'] = dimensions
            context['file_type'] = puremagic.magic_file(filename)[0].name 
            context['file_size'] = str(os.path.getsize(filename)) + ' bytes'
            context['filename'] = final_filename
            context['extension'] = puremagic.magic_file(filename)[0].extension
            context['mime_type'] = puremagic.magic_file(filename)[0].mime_type
            context['byte_match'] = puremagic.magic_file(filename)[0].byte_match.decode('UTF-8','ignore').strip()
            context['download'] = PayloadModel.objects.get(payload_user=request.user).payload_image
            context['status'] = 'Injected successfully'
            context['success_message'] = 'Your payload has been injected successfully!'
            return render(request, 'dashboard/injector.html', context)
        elif 'clear' in request.POST.keys():
            context['status'] = 'Cleared'
        else:
            context['status'] = 'Not injected'
        context['ipaddress'] = ip_address
        context['hex_dump'] = ''
        context['profile_account'] = request.user.profile
        context['dimensions'] = '(0, 0)'
        context['file_type'] = 'None'
        context['file_size'] = '0 bytes'
        context['filename'] = 'None'
        context['extension'] = 'None'
        context['mime_type'] = 'None'
        context['byte_match'] = 'None'
        return render(request, 'dashboard/injector.html', context)
    else:
        context['hex_dump'] = ''
        context['ipaddress'] = ip_address
        context['profile_account'] = request.user.profile
        context['dimensions'] = '(0, 0)'
        context['file_type'] = 'None'
        context['file_size'] = '0 bytes'
        context['filename'] = 'None'
        context['extension'] = 'None'
        context['mime_type'] = 'None'
        context['byte_match'] = 'None'
        context['status'] = 'Not injected'
    return render(request, 'dashboard/injector.html', context)

def post(request):
    return render(request, 'posts/post1.html')