from django.contrib import admin
from django.urls import path, include
from panol.views import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),  # <--- Agrega esta línea aquí
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", include("panol.urls")),
]