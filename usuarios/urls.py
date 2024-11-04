from django.urls import path
from .views import (
    LoginView,
    CadastroView,
    ValidaCadastroView,
    ValidarLoginView,
    SairView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("cadastro/", CadastroView.as_view(), name="cadastro"),
    path("validar_cadastro/", ValidaCadastroView.as_view(), name="valida_cadastro"),
    path("validar_login/", ValidarLoginView.as_view(), name="validar_login"),
    path("sair/", SairView.as_view(), name="sair"),
]
