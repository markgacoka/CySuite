from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from cyauth.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, widget=forms.EmailInput)

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "company", "role", "username", "password1", "password2")
        error_messages = {
            'first_name': {
                'required': ("First name is a required field."),
            },
            'last_name': {
                'required': ("Last name is a required field."),
            },
            'email': {
                'required': ("The email field is a required field."),
            },
            'username': {
                'required': ("Username is a required field."),
            },
            'password1': {
                'required': ("The password field is a required field."),
            },
            'password2': {
                'required': ("The password field is a required field."),
            },
        }

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        error_messages={
            'required': 'The password field is required to sign in.'
        }
    )

    class Meta:
        model = Account
        fields = ('email', 'password')
        error_messages = {
            'email': {
                'required': ("An email address is required to sign in."),
            }
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Email or password is incorrect')
            
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            username = self.cleaned_data['username']
            qs_username = Account.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
            qs_email = Account.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if qs_username.exists():
                raise forms.ValidationError('Username is already in use')
            elif qs_email.exists():
                raise forms.ValidationError('Email is already in use')
            else:
                return {"email": email, "username": username}
        return None

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['feedback']

    def clean(self):
        if self.is_valid():
            feedback = self.cleaned_data['feedback']
            return {"feedback": feedback}

class PasswordUpdateForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['password']

    def clean(self):
        if self.is_valid():
            old_password = self.cleaned_data['old_password']
            password = self.cleaned_data.get('password')
            password_confirmation = self.cleaned_data.get('password_confirmation')

            if password != password_confirmation:
                raise forms.ValidationError('The new password(s) should match!')
            elif not Account.objects.get(username=self.instance.username).check_password(old_password):
                raise forms.ValidationError('The previous password entered is incorrect!')
            else:
                return {"password": make_password(password)}
            