from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from .models import UserProfile
from main.models import PayloadModel
from main.models import WordlistModel


@receiver(post_save, sender=Account) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(username=instance)
        PayloadModel.objects.create(payload_user=instance)
        WordlistModel.objects.create(wordlist_user=instance)

@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.payload.save()