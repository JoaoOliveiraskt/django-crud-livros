from django.views import View
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256

# Login view
class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('usuario'):
            return redirect('/livro/home/')
        status = request.GET.get('status')
        return render(request, self.template_name, {'status': status})

# Registration view
class CadastroView(TemplateView):
    template_name = 'cadastro.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('usuario'):
            return redirect('/livro/home/')
        status = request.GET.get('status')
        return render(request, self.template_name, {'status': status})

# Validate registration view
class ValidaCadastroView(View):
    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        usuario = Usuario.objects.filter(email=email)

        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            return redirect('/auth/cadastro/?status=1')

        if len(senha) < 8:
            return redirect('/auth/cadastro/?status=2')

        if usuario.exists():
            return redirect('/auth/cadastro/?status=3')

        try:
            hashed_senha = sha256(senha.encode()).hexdigest()
            Usuario.objects.create(nome=nome, senha=hashed_senha, email=email)
            return redirect('/auth/cadastro/?status=0')
        except Exception:
            return redirect('/auth/cadastro/?status=4')

# Validate login view
class ValidarLoginView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        hashed_senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario.objects.filter(email=email, senha=hashed_senha)

        if not usuario.exists():
            return redirect('/auth/login/?status=1')
        else:
            request.session['usuario'] = usuario[0].id
            return redirect('/livro/home/')

# Logout view
class SairView(RedirectView):
    url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)
