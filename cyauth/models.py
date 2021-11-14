import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class MyUserManager(UserManager):
    def create_user(self, email, username, password=None):
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
        user.is_premium = True
        user.first_name = 'Admin'
        user.last_name = 'Account'
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, blank=False, unique=True, default=uuid.uuid4, db_index=True, editable=False)
    first_name = models.CharField(max_length=30, unique=False, null=True)
    last_name = models.CharField(max_length=30, unique=False, null=True)    
    username = models.CharField(max_length=64, unique=True)
    occupation = models.CharField(default='Researcher', max_length=64, unique=False, null=True, blank=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    image = models.TextField(default='default.jpeg', max_length=250, unique=False, null=False, blank=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    feedback = models.CharField(max_length= 1200, default= "", unique=False, null=True, blank=True)
    api_token = models.CharField(max_length=64, unique=False, null=True, blank=True)
    payload_image = models.ImageField(default='https://cysuite-bucket.s3.us-west-2.amazonaws.com/media/default.png', upload_to='payloads/', blank=True, null=True)
    badges = ArrayField(models.CharField(max_length=3000, blank=True), blank=True, null=True, default=list)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'people'
        abstract = False

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        else:
            return 'You'

    def __str__(self):
        return self.username