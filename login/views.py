from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy


class RegistroUsuario(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'login/registro.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'login/registro.html', {'form': form})
    
class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    authentication_form = CustomAuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, 'El usuario no está registrado o la contraseña es incorrecta.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('inventory-home')