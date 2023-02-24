from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Registeration form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is invalid')
        if len(email) >= 350:
            raise forms.ValidationError('This email is too long')
        return email


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Update form
class UpdateUserForm(forms.ModelForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta:
        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password1']