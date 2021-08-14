import re
import subprocess
import puremagic
import urllib.parse
import os, json, base64, requests
from html import escape, unescape
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TransactionForm
from .forms import ProjectForm
from .models import PayloadModel
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
    if request.method == 'POST':
        context['profile_account'] = request.user.profile
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            print(project_form.cleaned_data)
            print(request.user)
            project_form.project_user = request.user
            project_form.progress = 100
            project_form.subdomains = []
            project_form.save()
            context['success_message'] = 'Project has been created!'
            context['project_form'] = project_form
        else:
            context['error_message'] = 'An error occurred!'
    else:
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/projects.html', context)

def notes(request):
    context = {}
    context['profile_account'] = request.user.profile
    return render(request, 'dashboard/notes.html', context)

def subdomain_enum(request):
    context = {}
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
        url = request.POST.get('req_url')
        method = request.POST.get('req-method')
        req_header, resp_header = send_request(request, url, method)
        context['request_output'] = req_header
        context['response_output'] = resp_header
        context['profile_account'] = request.user.profile
    else:
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/req_tamperer.html', context)

def wordlist_gen(request):
    context = {}
    if request.method == 'POST':
        wordlist_url = request.POST.get('wordlist_url')
        wordlist = extract_wordlist(wordlist_url)
        context['wordlist_output'] = wordlist
        context['profile_account'] = request.user.profile
    else:
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

def file_upload(request):
    context = {}
    ip_address = get_client_ip(request)

    if request.method == "POST":
        payload = request.POST.get('payload').encode() if request.POST.get('payload') != None else None
        width = int(request.POST.get('width')) if request.POST.get('width') != '' and request.POST.get('width') != None else 0
        height = int(request.POST.get('height')) if request.POST.get('height') != '' and request.POST.get('width') != None else 0
        file_type = request.POST.get('file_type') if request.POST.get('file_type') != None else None
        filename = 'media/payloads/' + request.POST.get('filename') if request.POST.get('filename') != None else None
        
        injection = Injector(file_type, width, height, payload, filename)
        filename, dimensions = injection.main()
        if 'clear' in request.POST.keys():
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
            context['status'] = 'Cleared'
            return render(request, 'dashboard/file_upload.html', context)
        else:
            if 'full_hex' in request.POST.keys():
                from django.template.context_processors import csrf
                payload_file = PayloadModel.objects.get(payload_user=request.user)
                filename = payload_file.payload_image.path
                hex_dump = next(full_hex_viewer(filename))
                context['hex_dump'] = hex_dump
                context['ipaddress'] = ip_address
                context['profile_account'] = request.user.profile
                context['dimensions'] = '(0, 0)'
                context['file_type'] = puremagic.magic_file(filename)[0].name 
                context['file_size'] = str(os.path.getsize(filename)) + ' bytes'
                context['filename'] = re.sub(r'^.*?/', '', payload_file.payload_image.path)
                context['extension'] = puremagic.magic_file(filename)[0].extension
                context['mime_type'] = puremagic.magic_file(filename)[0].mime_type
                context['byte_match'] = puremagic.magic_file(filename)[0].byte_match.decode('UTF-8','ignore').strip()
                context['download'] = PayloadModel.objects.get(payload_user=request.user).payload_image
                context['status'] = 'Injected successfully'
                context.update(csrf(request))
                return render(request, 'dashboard/file_upload.html', context)
            elif filename != None or dimensions != None:
                new_filename = re.sub(r'^.*?/', '', filename)
                payload_file = PayloadModel.objects.get(payload_user=request.user)
                if new_filename != payload_file.payload_image.path:
                    os.remove(payload_file.payload_image.path)
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
        return render(request, 'dashboard/file_upload.html', context)
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
    return render(request, 'dashboard/file_upload.html', context)

def post(request):
    return render(request, 'posts/post1.html')