from datetime import date, datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria
from .forms import CadastroLivro, CategoriaLivro
from django import forms


# Create your views here.
def home(request):
    if request.session.get("usuario"):
        usuario = Usuario.objects.get(id=request.session["usuario"])
        status_categoria = request.GET.get("cadastro_categoria")
        livros = Livros.objects.filter(usuario=usuario)
        form = CadastroLivro()
        form.fields["usuario"].initial = request.session["usuario"]
        form.fields["categoria"].queryset = Categoria.objects.filter(usuario=usuario)
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()
        return render(
            request,
            "home.html",
            {
                "livros": livros,
                "usuario_logado": request.session.get("usuario"),
                "form": form,
                "status_categoria": status_categoria,
                "form_categoria": form_categoria,
                "usuarios": usuarios,
            },
        )
    else:
        return redirect("/auth/login/?status=2")


def ver_livros(request, id):
    if request.session.get("usuario"):
        livro = Livros.objects.get(id=id)
        if request.session.get("usuario") == livro.usuario.id:
            usuario = Usuario.objects.get(id=request.session["usuario"])
            categoria_livro = Categoria.objects.filter(
                usuario=request.session.get("usuario")
            )
            form = CadastroLivro()
            form.fields["usuario"].initial = request.session["usuario"]
            form.fields["categoria"].queryset = Categoria.objects.filter(
                usuario=usuario
            )
            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()
            return render(
                request,
                "ver_livro.html",
                {
                    "livro": livro,
                    "categoria_livro": categoria_livro,
                    "usuario_logado": request.session.get("usuario"),
                    "form": form,
                    "id_livro": id,
                    "form_categoria": form_categoria,
                    "usuarios": usuarios,
                },
            )
        else:
            return HttpResponse("Esse livro não é seu")
    return redirect("/auth/login/?status=2")


def cadastrar_livro(request):
    if request.method == "POST":
        form = CadastroLivro(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/livro/home")
        else:
            return HttpResponse("DADOS INVÁLIDOS")


def excluir_livro(request, id):
    livro = Livros.objects.get(id=id).delete()
    return redirect("/livro/home")


def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data["nome"]
    descricao = form.data["descricao"]
    id_usuario = request.POST.get("usuario")
    if int(id_usuario) == int(request.session.get("usuario")):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect("/livro/home?cadastro_categoria=1")
    else:
        return HttpResponse(" Não foi desta vez.")


def alterar_livro(request):
    livro_id = request.POST.get("livro_id")
    nome_livro = request.POST.get("nome_livro")
    autor = request.POST.get("autor")
    co_autor = request.POST.get("co_autor")
    descricao = request.POST.get("descricao")
    categoria_id = request.POST.get("categoria_id")
    categoria = Categoria.objects.get(id=categoria_id)
    livro = Livros.objects.get(id=livro_id)
    if livro.usuario.id == request.session["usuario"]:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.descricao = descricao
        livro.save()
        return redirect(f"/livro/ver_livro/{livro_id}")
    else:
        return redirect("/auth/sair")
