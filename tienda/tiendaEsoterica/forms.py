from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class CustomUserCreationForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Introduce tu correo'}),
    )
    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce tu contraseña'}),
        help_text="Debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.",
    )
    password2 = forms.CharField(
        label="Confirmación de Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu contraseña'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe incluir al menos un número.")
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Correo o contraseña incorrectos.")
        return super().clean()