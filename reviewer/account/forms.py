from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.core.exceptions import ValidationError

from .models import CustomUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
# from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomUserAuthenticationForm(forms.ModelForm):
    email = forms.CharField(max_length=150,
                            widget=forms.TextInput(attrs={'placeholder': _("Email"), 'class': 'form-control'}),
                            help_text="email")
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'placeholder': _("Password"), 'class': 'form-control'}),
                               help_text="password")

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(_("Invalid login"), code='invalid')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "email", "first_name", "last_name", "gender", "birthday", "user_language", "photo")

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Email")}),
            # 'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Username")}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _("First name"), 'required': 'false'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Last name")}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthday': DateInput(attrs={'type': 'text', 'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1', 'id': 'datetimepicker1'}),
            'user_language': forms.Select(attrs={'class': 'form-control'}),
            # 'photo': forms.FileInput(attrs={'capture': 'camera'}),
        }

    def clean_email(self):
        print('Start')
        print(self.cleaned_data['email'])
        print(self.is_valid())

        email = self.cleaned_data['email']

        try:
            user = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError(_('Email "%s" is already in use.') % user.email)


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creats a custom user with no privilages
    form a provided email and password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = '__all__'