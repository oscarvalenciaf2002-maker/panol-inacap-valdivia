from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Usuario, Asignatura, Categoria

def login_view(request):
    if request.method == "POST":
        rut = request.POST.get("rut", "").strip()
        usuario = Usuario.objects.filter(rut=rut).first()
        if usuario:
            request.session["usuario_id"] = usuario.id_usuario
            request.session["tipo_usuario"] = usuario.tipo_usuario
            return redirect("/panolero/" if request.POST.get("rol") == "panolero" else "/usuario/")
        return render(request, "login.html", {"error": "RUT no encontrado en la base de datos."})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("/")

def _ctx(request):
    uid = request.session.get("usuario_id")
    user = Usuario.objects.filter(pk=uid).first() if uid else None
    return {"usuario": user}

def usuario_dashboard(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "usuario/dashboard.html", _ctx(request))

def nueva_solicitud(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "usuario/nueva_solicitud.html", _ctx(request))

def mis_prestamos(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "usuario/prestamos.html", _ctx(request))

def panolero_dashboard(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "panolero/dashboard.html", _ctx(request))

def panolero_prestamos(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "panolero/prestamos.html", _ctx(request))

def meson(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "panolero/meson.html", _ctx(request))

def inventario(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "panolero/inventario.html", _ctx(request))

def mermas(request):
    if not request.session.get("usuario_id"): return redirect("/")
    return render(request, "panolero/mermas.html", _ctx(request))
