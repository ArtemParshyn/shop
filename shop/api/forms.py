from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-lg shadow-sm border-gray-300',
            'placeholder': 'Enter your username',
            'minlength': 3,
            'required': True,
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-lg shadow-sm border-gray-300',
            'placeholder': 'Enter your password',
            'minlength': 8,
            'required': True,
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-lg shadow-sm border-gray-300',
            'placeholder': 'Confirm your password',
            'required': True,
        })
    )

    class Meta:
        model = get_user_model()  # Подключаем вашу кастомную модель
        fields = ('username', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'block w-full transition duration-75 rounded-lg shadow-sm focus:border-primary-500 focus:ring-1 '
                 'focus:ring-inset focus:ring-primary-500 disabled:opacity-70 border-gray-300',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full transition duration-75 rounded-lg shadow-sm focus:border-primary-500 focus:ring-1 '
                 'focus:ring-inset focus:ring-primary-500 disabled:opacity-70 border-gray-300',
        'placeholder': 'Password'
    }))

    class Meta:
        model = get_user_model()  # Подключаем вашу кастомную модель
        fields = ('username', 'password')
