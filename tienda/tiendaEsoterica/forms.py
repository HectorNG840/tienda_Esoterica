from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Perfil
from django.core.validators import RegexValidator


class CustomUserCreationForm(forms.Form):
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tu nombre'}),
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tus apellidos'}),
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Introduce tu correo'}),
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d+$',
                message="El número de teléfono debe contener solo dígitos."
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tu número de teléfono'}),
    )
    direccion = forms.CharField(
        label="Dirección",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tu dirección'}),
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )
    codigo_postal = forms.CharField(
        label="Código Postal",
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$', 
                message="El código postal solo debe contener números."
             )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tu código postal'}),
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


class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'fecha_nacimiento', 'codigo_postal']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu dirección'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu código postal'}),
        }


class EnvioForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    direccion_envio = forms.CharField(widget=forms.Textarea)
    ciudad = forms.CharField(max_length=100)
    codigo_postal = forms.CharField(max_length=10)
    pais = forms.CharField(max_length=100)


class PagoForm(forms.Form):
    numero_tarjeta = forms.CharField(max_length=16, label="Número de Tarjeta")
    fecha_expiracion = forms.CharField(max_length=5, label="Fecha de Expiración (MM/AA)")
    cvv = forms.CharField(max_length=3, label="CVV")
    nombre_titular = forms.CharField(max_length=100, label="Nombre del Titular")
