from django import forms
from django.db import models
from .models import Transaction
from .models import Newsletter

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_account', 'given_name', 'last_name', 'payer_email', 'amount', 'currency', 'status', 'transaction_code']

    def clean(self):
        if self.is_valid():
            user_account = self.cleaned_data['user_account']
            given_name = self.cleaned_data['given_name']
            last_name = self.cleaned_data['last_name']
            payer_email = self.cleaned_data['payer_email']
            amount = self.cleaned_data['amount']
            currency = self.cleaned_data['currency']
            status = self.cleaned_data['status']
            transaction_code = self.cleaned_data['transaction_code']
            return {
                "user_account": user_account,
                "given_name": given_name,
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
