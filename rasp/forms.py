# -*- coding: utf-8 -*-
from django import forms
from .models import ResponseOnTask
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):

    class Meta:
        model = ResponseOnTask
        fields = ('intro_text_responce', 'responce_text')
        widgets = {'user_responce': forms.HiddenInput(), 'responce_task': forms.HiddenInput()}


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.all().filter(username=username).exists():
            raise forms.ValidationError('Пользователя с данным именем не существует')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')

