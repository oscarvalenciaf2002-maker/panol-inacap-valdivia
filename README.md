# Pañol INACAP Valdivia

Sistema web Full Stack para digitalizar solicitudes, préstamos, devoluciones, inventario y mermas del Pañol/Laboratorio.

## Stack
- Backend: Django 5 + Django REST Framework
- Base de datos: PostgreSQL
- Frontend: Django Templates + Tailwind CSS CDN + JavaScript
- Roles: Alumno/Docente y Pañolero

## 1. Instalación

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Copia `.env.example` como `.env` y configura PostgreSQL:

```env
DB_NAME=panol_inacap
DB_USER=postgres
DB_PASSWORD=tu_clave
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=cambia-esta-clave
DEBUG=True
```

El proyecto usa `managed=False` para respetar las tablas existentes. **No ejecutes migraciones sobre las 11 tablas del esquema entregado.**

```bash
python manage.py runserver
```

Abre:
- Portal usuario: `/`
- Portal pañolero: `/panolero/`
- API: `/api/`

## 2. Esquema de estados

La BD existente solamente tiene E/D/P en `detalle_prestamo`. Por eso la aplicación usa una capa de estados de interfaz:

- Solicitud nueva: `firma_panolero = PENDIENTE`
- Aprobada/lista para retirar: `firma_panolero = APROBADO`
- Entregada: detalle `E`
- En uso/pendiente de devolución: detalle `P`
- Devuelta: detalle `D`

Esto permite ofrecer el flujo solicitado sin alterar el ENUM existente. En una segunda versión, lo ideal es agregar `estado_solicitud` a `solicitudes_prestamo` para tener estados explícitos.

## 3. Importante para producción

El acceso por RUT incluido es un modo demostrativo. Para una implementación institucional real debe sustituirse por SSO/credenciales institucionales o un proveedor de identidad.

## 4. Estructura

```text
panol_inacap/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── panol/
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── api.py
│   └── serializers.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── usuario/
│   │   ├── dashboard.html
│   │   ├── nueva_solicitud.html
│   │   └── prestamos.html
│   └── panolero/
│       ├── dashboard.html
│       ├── prestamos.html
│       ├── meson.html
│       ├── inventario.html
│       └── mermas.html
└── static/js/
    ├── app.js
    ├── usuario.js
    └── panolero.js
```
