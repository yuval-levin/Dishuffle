from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from . import models


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    # these attributes are important for register.html, so we can override the {{field}} in form and use the google
    # maps autocomplete API
    address = forms.CharField(max_length=120, widget=forms.TextInput(attrs=
                                                                     {'placeholder': 'Enter address',
                                                                      'id': 'address', 'name': 'address',
                                                                      'type': 'address'}
                                                                     ))

    class Meta:
        model = models.Account
        fields = ('email', 'username', 'address', 'password1', 'password2','latitude','longitude')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = models.Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                pdb.set_trace()
                raise forms.ValidationError("Login failed. Check your email and password")


class AccountUpdateForm(forms.ModelForm):
    latitude = forms.DecimalField(widget = forms.HiddenInput(),required = False)
    longitude = forms.DecimalField(widget = forms.HiddenInput(),required = False)

    class Meta:
        model = models.Account
        fields = ('email', 'username', 'address','latitude','longitude')

    # update email
    # we accept multiple users with same email address, hence no checking if user with same email exists
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    # updates address in form
    # we accept multiple users with same address, hence no checking if user with same address exists.
    def clean_address(self):
        address = self.cleaned_data['address']
        return address

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        return longitude

    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        return latitude

    # validates and updates username in form
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = models.Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except models.Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
