from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("livro/", include("livro.urls")),  # Inclui as URLs do app 'livro'
    path("auth/", include("usuarios.urls")),  # Inclui as URLs do app 'usuarios'
    path(
        "", RedirectView.as_view(url="/livro/home/", permanent=False)
    ),  # Redireciona para '/livro/home/'
]
