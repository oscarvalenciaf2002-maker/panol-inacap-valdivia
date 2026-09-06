from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction, connection
from django.utils import timezone
from .models import (
    Usuario, Articulo, Categoria, Asignatura, SolicitudPrestamo,
    DetallePrestamo, InventarioDetalle, Merma, ArticuloAsignatura
)

def uid(request):
    return request.session.get("usuario_id")

def dashboard_api(request):
    activos = DetallePrestamo.objects.filter(estado_prestamo="P").count()
    entregados = DetallePrestamo.objects.filter(
        estado_prestamo="D", fecha_devolucion__date=timezone.localdate()
    ).count()
    mermas = Merma.objects.count()
    fuera = InventarioDetalle.objects.filter(cantidad_bueno__lte=0).count()

    ultimas = SolicitudPrestamo.objects.select_related("id_usuario", "id_asignatura").order_by("-fecha_solicitud")[:5]
    rows = [{
        "id": x.id_solicitud,
        "solicitante": f"{x.id_usuario.nombre} {x.id_usuario.apellido_paterno}",
        "asignatura": x.id_asignatura.nombre_asignatura,
        "fecha": x.fecha_solicitud.strftime("%d/%m/%Y %H:%M"),
        "estado": "APROBADO" if x.firma_panolero == "APROBADO" else "PENDIENTE"
    } for x in ultimas]

    return JsonResponse({
        "activos": activos,
        "devueltos_hoy": entregados,
        "mermas": mermas,
        "fuera_stock": fuera,
        "ultimas": rows
    })

def catalogo_api(request):
    q = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    qs = Articulo.objects.select_related("id_categoria").all().order_by("nombre_articulo")
    if q:
        qs = qs.filter(nombre_articulo__icontains=q)
    if categoria.isdigit():
        qs = qs.filter(id_categoria_id=int(categoria))
    data = []
    for a in qs:
        inv = InventarioDetalle.objects.filter(pk=a.id_articulo).first()
        prestado = DetallePrestamo.objects.filter(id_articulo=a, estado_prestamo="P").values_list("cantidad", flat=True)
        prestado_total = sum(prestado)
        data.append({
            "id": a.id_articulo,
            "codigo": a.codigo_peoplesoft or "",
            "nombre": a.nombre_articulo,
            "categoria": a.id_categoria.nombre_categoria,
            "lugar": a.lugar_almacenamiento or "",
            "stock": inv.cantidad_existente if inv else 0,
            "bueno": inv.cantidad_bueno if inv else 0,
            "reparable": inv.cantidad_reparable if inv else 0,
            "malo": inv.cantidad_malo if inv else 0,
            "disponible": max((inv.cantidad_bueno if inv else 0) - prestado_total, 0)
        })
    return JsonResponse({"items": data, "categorias": list(Categoria.objects.values("id_categoria","nombre_categoria"))})

def asignaturas_api(request):
    return JsonResponse({"items": list(Asignatura.objects.values("id_asignatura","codigo_asignatura","nombre_asignatura").order_by("nombre_asignatura"))})

@require_http_methods(["GET","POST"])
def solicitudes_api(request):
    if request.method == "GET":
        qs = SolicitudPrestamo.objects.select_related("id_usuario","id_asignatura").order_by("-fecha_solicitud")
        if request.session.get("usuario_id"):
            qs = qs.filter(id_usuario_id=request.session["usuario_id"])
        data=[]
        for s in qs:
            detalles = DetallePrestamo.objects.filter(id_solicitud=s).select_related("id_articulo")
            data.append({
                "id": s.id_solicitud,
                "fecha": s.fecha_solicitud.strftime("%d/%m/%Y %H:%M"),
                "asignatura": s.id_asignatura.nombre_asignatura,
                "seccion": s.seccion,
                "docente": s.nombre_docente,
                "estado_solicitud": "LISTO PARA RETIRAR" if s.firma_panolero=="APROBADO" else "PENDIENTE DE APROBACIÓN",
                "items": [{"id":d.id_articulo_id,"nombre":d.id_articulo.nombre_articulo,"cantidad":d.cantidad,"estado":d.estado_prestamo} for d in detalles]
            })
        return JsonResponse({"items":data})

    import json
    body = json.loads(request.body or "{}")
    usuario_id = uid(request)
    if not usuario_id:
        return JsonResponse({"error":"Sesión requerida"}, status=401)

    items = body.get("items", [])
    if not items or len(items) > 10:
        return JsonResponse({"error":"La solicitud debe tener entre 1 y 10 ítems."}, status=400)

    with transaction.atomic():
        solicitud = SolicitudPrestamo.objects.create(
            id_usuario_id=usuario_id,
            id_asignatura_id=body["id_asignatura"],
            seccion=body["seccion"],
            nombre_docente=body["nombre_docente"],
            fecha_solicitud=timezone.now(),
            firma_solicitante=bool(body.get("firma_solicitante", True)),
            firma_panolero="PENDIENTE",
        )
        for item in items:
            art = Articulo.objects.get(pk=int(item["id_articulo"]))
            cantidad = int(item["cantidad"])
            if cantidad < 1: raise ValueError("Cantidad inválida")
            inv = InventarioDetalle.objects.filter(pk=art.id_articulo).first()
            if not inv or inv.cantidad_bueno < cantidad:
                raise ValueError(f"Stock insuficiente para {art.nombre_articulo}")
            DetallePrestamo.objects.create(
                id_solicitud=solicitud,
                id_articulo=art,
                cantidad=cantidad,
                estado_prestamo="E"
            )
    return JsonResponse({"ok":True,"id_solicitud":solicitud.id_solicitud}, status=201)

@require_http_methods(["POST"])
def aprobar_solicitud_api(request, pk):
    if not request.session.get("usuario_id"):
        return JsonResponse({"error":"Sesión requerida"}, status=401)
    with transaction.atomic():
        s = SolicitudPrestamo.objects.get(pk=pk)
        s.firma_panolero = "APROBADO"
        s.save(update_fields=["firma_panolero"])
    return JsonResponse({"ok":True})

@require_http_methods(["GET","POST"])
def prestamos_api(request):
    qs = DetallePrestamo.objects.select_related("id_solicitud__id_usuario","id_articulo").order_by("-id_detalle_prestamo")
    if request.method=="GET":
        data=[]
        for d in qs:
            data.append({
                "id":d.id_detalle_prestamo,
                "solicitud":d.id_solicitud_id,
                "solicitante":f"{d.id_solicitud.id_usuario.nombre} {d.id_solicitud.id_usuario.apellido_paterno}",
                "articulo":d.id_articulo.nombre_articulo,
                "cantidad":d.cantidad,
                "estado":d.estado_prestamo,
                "fecha_devolucion":d.fecha_devolucion.strftime("%d/%m/%Y %H:%M") if d.fecha_devolucion else None
            })
        return JsonResponse({"items":data})

@require_http_methods(["POST"])
def devolucion_api(request, pk):
    import json
    body=json.loads(request.body or "{}")
    with transaction.atomic():
        d=DetallePrestamo.objects.get(pk=pk)
        d.estado_prestamo="D"
        d.fecha_devolucion=timezone.now()
        d.vbo_panol=body.get("vbo_panol") or "Pañolero"
        d.save(update_fields=["estado_prestamo","fecha_devolucion","vbo_panol"])
        obs=body.get("observaciones","").strip()
        if obs:
            inv=InventarioDetalle.objects.filter(pk=d.id_articulo_id).first()
            if inv:
                inv.observaciones=obs
                inv.save(update_fields=["observaciones"])
    return JsonResponse({"ok":True})

@require_http_methods(["GET","POST"])
def mermas_api(request):
    if request.method=="GET":
        qs=Merma.objects.select_related("id_articulo").order_by("-id_merma")
        return JsonResponse({"items":[{
            "id":m.id_merma,"articulo":m.id_articulo.nombre_articulo,
            "periodo":m.periodo_academico,"tipo":m.tipo_merma,
            "cantidad":m.cantidad,"observaciones":m.observaciones or ""
        } for m in qs]})

    import json
    b=json.loads(request.body or "{}")
    m=Merma.objects.create(
        id_articulo_id=int(b["id_articulo"]),
        periodo_academico=b["periodo_academico"],
        marca=b.get("marca",""),
        modelo_serie=b.get("modelo_serie",""),
        tipo_merma=b["tipo_merma"],
        cantidad=int(b.get("cantidad",1)),
        observaciones=b.get("observaciones","")
    )
    return JsonResponse({"ok":True,"id":m.id_merma}, status=201)
