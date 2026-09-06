from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, unique=True)
    class Meta:
        managed = False
        db_table = "categorias"

class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    codigo_carrera = models.CharField(max_length=20, unique=True)
    nombre_carrera = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = "carreras"

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    codigo_asignatura = models.CharField(max_length=20, unique=True)
    nombre_asignatura = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = "asignaturas"

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = "usuarios"

class Articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categoria, db_column="id_categoria", on_delete=models.RESTRICT)
    codigo_peoplesoft = models.CharField(max_length=50, null=True, blank=True)
    nombre_articulo = models.CharField(max_length=255)
    especificacion_tecnica = models.TextField(null=True, blank=True)
    lugar_almacenamiento = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        managed = False
        db_table = "articulos"

class InventarioDetalle(models.Model):
    id_articulo = models.OneToOneField(Articulo, db_column="id_articulo", primary_key=True, on_delete=models.CASCADE)
    cantidad_existente = models.IntegerField(default=0)
    cantidad_estandar_necesaria = models.IntegerField(default=0)
    cantidad_bueno = models.IntegerField(default=0)
    cantidad_reparable = models.IntegerField(default=0)
    cantidad_malo = models.IntegerField(default=0)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = "inventario_detalles"

class Merma(models.Model):
    id_merma = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, db_column="id_articulo", on_delete=models.RESTRICT)
    periodo_academico = models.CharField(max_length=20)
    marca = models.CharField(max_length=100, null=True, blank=True)
    modelo_serie = models.CharField(max_length=100, null=True, blank=True)
    tipo_merma = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=1)
    observaciones = models.TextField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = "mermas_registro"

class SolicitudPrestamo(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, db_column="id_usuario", on_delete=models.RESTRICT)
    id_asignatura = models.ForeignKey(Asignatura, db_column="id_asignatura", on_delete=models.RESTRICT)
    seccion = models.CharField(max_length=20)
    nombre_docente = models.CharField(max_length=150)
    fecha_solicitud = models.DateTimeField()
    firma_solicitante = models.BooleanField(default=True)
    firma_panolero = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = "solicitudes_prestamo"

class DetallePrestamo(models.Model):
    id_detalle_prestamo = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SolicitudPrestamo, db_column="id_solicitud", on_delete=models.CASCADE)
    id_articulo = models.ForeignKey(Articulo, db_column="id_articulo", on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    estado_prestamo = models.CharField(max_length=1, default="P")
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    vbo_panol = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        managed = False
        db_table = "detalle_prestamo"

class ArticuloCarrera(models.Model):
    id_articulo = models.ForeignKey(Articulo, db_column="id_articulo", on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carrera, db_column="id_carrera", on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = "articulo_carreras"
        unique_together = (("id_articulo", "id_carrera"),)

class ArticuloAsignatura(models.Model):
    id_articulo = models.ForeignKey(Articulo, db_column="id_articulo", on_delete=models.CASCADE)
    id_asignatura = models.ForeignKey(Asignatura, db_column="id_asignatura", on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = "articulo_asignaturas"
        unique_together = (("id_articulo", "id_asignatura"),)
