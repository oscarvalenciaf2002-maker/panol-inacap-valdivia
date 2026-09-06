from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("usuario/", views.usuario_dashboard, name="usuario_dashboard"),
    path("usuario/solicitud/", views.nueva_solicitud, name="nueva_solicitud"),
    path("usuario/prestamos/", views.mis_prestamos, name="mis_prestamos"),

    path("panolero/", views.panolero_dashboard, name="panolero_dashboard"),
    path("panolero/prestamos/", views.panolero_prestamos, name="panolero_prestamos"),
    path("panolero/meson/", views.meson, name="meson"),
    path("panolero/inventario/", views.inventario, name="inventario"),
    path("panolero/mermas/", views.mermas, name="mermas"),

    path("api/dashboard/", api.dashboard_api),
    path("api/catalogo/", api.catalogo_api),
    path("api/asignaturas/", api.asignaturas_api),
    path("api/solicitudes/", api.solicitudes_api),
    path("api/solicitudes/<int:pk>/aprobar/", api.aprobar_solicitud_api),
    path("api/prestamos/", api.prestamos_api),
    path("api/prestamos/<int:pk>/devolucion/", api.devolucion_api),
    path("api/mermas/", api.mermas_api),
]
