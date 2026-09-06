from django.urls import path, include
from panol.views import login_view, logout_view

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", include("panol.urls")),
]
