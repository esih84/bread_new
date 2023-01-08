from django import forms
from .models import User, profile, buy
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('PLEASE CHECK THE PASSWORD')
        return data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_password(self):
        return self.initial['password']


class UserProfileUpdate(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['first_name', 'last_name', 'phone', 'city', 'address']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['email', 'username']


class buy_form(forms.ModelForm):
    class Meta:
        model=buy
        fields = ['bread_count', 'discount']
