from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from cyauth.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, widget=forms.EmailInput)

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

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