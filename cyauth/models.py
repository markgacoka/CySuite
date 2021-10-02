import hashlib
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from six import python_2_unicode_compatible
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from allauth.account.signals import user_signed_up


class MyUserManager(UserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("You must have a email to continue!")
        if not username:
            raise ValueError("You must have a username to continue!")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_premium = True
        user.given_name = 'Admin'
        user.family_name = 'Account'
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, blank=False, unique=True, default=uuid.uuid4, db_index=True, editable=False)
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=60,
        unique=True
    )
    given_name = models.CharField(max_length=30, unique=False, null=True)
    family_name = models.CharField(max_length=30, unique=False, null=True)    
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    feedback = models.CharField(max_length= 1200, default= "", unique=False, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'people'
        abstract = False

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    @property
    def name(self):
        if self.given_name:
            return self.given_name
        elif self.name:
            return self.name
        else:
            return 'You'

    def get_full_name(self):
        """
        Returns the given_name plus the family_name, with a space in between.
        """
        full_name = '%s %s' % (self.given_name, self.family_name)
        return full_name.strip()

    def get_short_name(self):
        return self.given_name

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.name:
            return

        if self.given_name and self.family_name:
            dn = "%s %s" % (self.given_name, self.family_name[0])  # like "Andrew E"
        elif self.given_name:
            dn = self.given_name
        else:
            dn = 'You'
        self.name = dn.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.email)


@python_2_unicode_compatible
class UserProfile(models.Model):
    username = models.OneToOneField(Account, primary_key=True, related_name='profile', db_column="user_id", on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profiles/', blank=True, null=True)

    class Meta():
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.username.name + 'Profile'