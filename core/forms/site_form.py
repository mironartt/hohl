from django import forms
from django.shortcuts import render
import sys
import traceback

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, SetPasswordForm
from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.template import loader
from django.utils import timezone

from core.models import User
from core.utils.text import get_translate_base as _


class CustomUserCreationForm(UserCreationForm):

    email = forms.CharField(max_length=150, required=True, widget=forms.EmailInput({'placeholder': 'E-mail'}))
    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    phone = forms.CharField(label='Телефон', max_length=20, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Телефон'}))
    first_name = forms.CharField(label='Имя', max_length=50, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=100, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Фамилия'}))
    country = forms.CharField(label='Страна', max_length=50, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Страна'}))
    address = forms.CharField(label='Адрес', max_length=500, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Адрес'}))
    post_code = forms.CharField(label='Индекс', max_length=20, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Индекс'}))
    city = forms.CharField(label='Город', max_length=20, required=True, strip=True, widget=forms.TextInput({'placeholder': 'Город'}))

    class Meta:
        model = User
        fields = ("email", 'phone', 'password1', 'password2', 'first_name', 'last_name', 'country', 'address', 'post_code', 'city')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Введенные пароли не совпадают!')

    def clean_password1(self):
        try:
            password_validation.validate_password(self.cleaned_data['password1'])
        except forms.ValidationError as error:
            for e in error.error_list:
                self.add_error('password1', e.message if '%(min_length)d' not in e.message else str(e.message).replace('%(min_length)d', '8'))
            return
        return self.cleaned_data['password1']

    def clean_phone(self):
        if not self.cleaned_data.get('phone') or len(str(self.cleaned_data['phone'])) < 5:
            self.add_error('phone', 'Указанный телефон слишком короткий')
        else:
            return self.cleaned_data['phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        val = EmailValidator()
        try:
            val(email)
        except ValidationError as e:
            raise forms.ValidationError(_(e.message, self.l_key))
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Пользователь с таким адресом электронной почты уже существует.')

    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        print('cleaned_data >>>>>>>>>>>>>>> ' + str(cleaned_data))
        return cleaned_data


class CustomAuthenticationForm(forms.Form):

    email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput({'placeholder': 'E-mail',}))
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    def clean(self):
        cleaned_data = super(CustomAuthenticationForm, self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email.strip())
            self.user = user if user and user.check_password(password) else False
            if self.user and self.user.confirm_email:
                return cleaned_data
            if not self.errors:
                self.add_error('email', 'указанный пользователь не найден, либо неверный пароль, либо email не был подтвержден')
        except:
            if not self.errors:
                self.add_error('email', 'указанный пользователь не найден, либо неверный пароль, либо email не был подтвержден')
        return False

    def get_user(self):
        return self.user


class RemindPasswordForm(forms.Form):

    email = forms.CharField(max_length=150, required=True, widget=forms.EmailInput({'placeholder': 'email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        val = EmailValidator()
        try:
            val(email)
        except ValidationError as e:
            raise forms.ValidationError(_(e.message, self.l_key))
        try:
            self.user = User.objects.get(email=email.strip())
            return email
        except User.DoesNotExist:
            raise forms.ValidationError('пользователь с таким адресом электронной почты не найден.')

    def get_user(self):
        return self.user


class RemindPasswordInputForm(forms.Form):

    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput({'placeholder': 'новый пароль',}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'повторите новый пароль'}))

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError('Введенные пароли не совпадают!')

    def clean_password1(self):
        try:
            password_validation.validate_password(self.cleaned_data['password1'])
        except forms.ValidationError as error:
            for e in error.error_list:
                self.add_error('password1', _(e.message if '%(min_length)d' not in e.message else str(e.message).replace('%(min_length)d', '8'), self.l_key))
            return
        return self.cleaned_data['password1']
