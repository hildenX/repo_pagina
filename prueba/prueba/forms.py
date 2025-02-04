# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from cine.models import Comentario

class RegistroForm(forms.Form):
    nombre = forms.CharField(min_length=2, max_length=100, label="Nombre")
    apellido = forms.CharField(min_length=2, max_length=100, label="Apellido")
    email = forms.EmailField(label="Correo Electrónico")
    contraseña = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmacion_contraseña = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmacion_contraseña = cleaned_data.get("confirmacion_contraseña")

        if contraseña != confirmacion_contraseña:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")
    contraseña = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        contraseña = cleaned_data.get("contraseña")

        if not User.objects.filter(email=email).exists():
            raise ValidationError("Este correo no está registrado.")
        user = User.objects.get(email=email)
        if not user.check_password(contraseña):
            raise ValidationError("Contraseña incorrecta.")
        return cleaned_data
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }