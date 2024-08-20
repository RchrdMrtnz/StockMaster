from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario o correo electrónico", max_length=254)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                try:
                    if '@' in username:
                        user = User.objects.get(email=username)
                        user = authenticate(username=user.username, password=password)
                except User.DoesNotExist:
                    raise forms.ValidationError("Usuario o contraseña incorrectos.")
                if not user:
                    raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return super().clean()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return password2
