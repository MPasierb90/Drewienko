from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class SignUpForm(UserCreationForm):
    # username = UsernameField(
    #     label="Nazwa użytkownika",
    #     widget=forms.TextInput(
    #         attrs={'autofocus': True,
    #                'class': 'form-control-lg pr-4 shadow-none',
    #                'placeholder': 'Nazwa uzytkownika'},
    #     ),
    # )
    # email = forms.EmailField(
    #     max_length=254, label='Email',
    #     widget=forms.EmailInput(
    #         attrs={'class': 'form-control-lg pr-4 shadow-none'}),
    #     validators=[EmailValidator]
    # )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')