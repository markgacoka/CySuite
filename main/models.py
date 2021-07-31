from django.db import models

class Transaction(models.Model):
    user_account = models.TextField(max_length=30, unique=False, null=False, default='None')
    given_name = models.TextField(max_length=50, blank=True, null=True)
    last_name = models.TextField(max_length=50, blank=True, null=True)
    payer_email = models.EmailField(max_length=254, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(max_length=10, blank=True, null=True)
    status = models.TextField(max_length=254, blank=True, null=True)
    transaction_code = models.TextField(max_length=50, blank=True, null=True, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)