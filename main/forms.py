from django import forms
from django.db import models
from .models import Transaction
from .models import Newsletter
from .models import ProjectModel
from .models import WordlistModel
from cyauth.models import Account
from django.conf import settings

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_account', 'first_name', 'last_name', 'payer_email', 'amount', 'currency', 'status', 'transaction_code']

    def clean(self):
        if self.is_valid():
            user_account = self.cleaned_data['user_account']
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            payer_email = self.cleaned_data['payer_email']
            amount = self.cleaned_data['amount']
            currency = self.cleaned_data['currency']
            status = self.cleaned_data['status']
            transaction_code = self.cleaned_data['transaction_code']
            return {
                "user_account": user_account,
                "first_name": first_name,
                "last_name": last_name,
                "payer_email": payer_email,
                "amount": amount,
                "currency": currency,
                "status": status,
                "transaction_code": transaction_code,
            }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subscriber']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['project_name', 'program', 'in_scope_domains']

class WordlistForm(forms.ModelForm):
    class Meta:
        model = WordlistModel
        fields = ['wordlist_file_3', 'wordlist_file_4', 'wordlist_file_5']
