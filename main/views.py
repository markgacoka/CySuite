import os, json
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
    return render(request, 'dashboard/decoder.html')

def file_upload(request):
    return render(request, 'dashboard/file_upload.html')

def post(request):
    return render(request, 'posts/post1.html')
