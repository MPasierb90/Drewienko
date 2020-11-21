from django import forms
from django.contrib.auth.forms import UserCreationForm, User
# from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from .models import UserProfile


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


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('city', 'phone_number', 'avatar')

    def save(self, commit=True):
        user_profile = super(UserProfileEditForm, self).save(commit=False)
        user_profile.city = self.cleaned_data['city']
        user_profile.phone_number = self.cleaned_data['phone_number']
        user_profile.avatar = self.cleaned_data['avatar']

        if commit:
            user_profile.save()

        return user_profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user
