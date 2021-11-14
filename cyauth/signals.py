from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from main.models import WordlistModel
from main.models import Newsletter

@receiver(post_save, sender=Account) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        WordlistModel.objects.create(wordlist_user=instance)
        Newsletter.objects.create(subscriber=instance)