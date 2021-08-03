import os, json, base64
from html import escape, unescape
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TransactionForm

def checkout(request):
    return render(request, 'pages/checkout.html', context={
        'PAYPAL_CLIENT_ID': os.environ.get('PAYPAL_CLIENT_ID'),
    })

def update_transaction(request):
    if request.method == 'POST':
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
    return render(request, 'dashboard/projects.html')

def notes(request):
    return render(request, 'dashboard/notes.html')

def subdomain_enum(request):
    return render(request, 'dashboard/subdomain_enum.html')

def directory_enum(request):
    return render(request, 'dashboard/directory_enum.html')

def vuln_analysis(request):
    return render(request, 'dashboard/vuln_analysis.html')
    
def dorking(request):
    return render(request, 'dashboard/dorking.html')

def exploit(request):
    return render(request, 'dashboard/exploits.html')

def req_tamperer(request):
    return render(request, 'dashboard/req_tamperer.html')

def wordlist_gen(request):
    return render(request, 'dashboard/wordlist_gen.html')

def decoder(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
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
            context['decode_output'] = str(request.POST.get('decode-string'))
        elif 'clear-encoder' in request.POST:
            context['encode_output'] = ''
            context['decode_output'] = str(request.POST.get('decode-string'))
        elif 'clear-decoder' in request.POST:
            context['decode_output'] = ''
            context['encode_output'] = str(request.POST.get('encode-string'))
        else:
            pass
    else:
        pass
    return render(request, 'dashboard/decoder.html', context)

def file_upload(request):
    return render(request, 'dashboard/file_upload.html')

def post(request):
    return render(request, 'posts/post1.html')
