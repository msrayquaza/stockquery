from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# ================ #
#    USUARIOS      #
# ================ #
class Usuarios(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=50,
        choices=[
            ('Administrador', 'Administrador'),
            ('Recepcion', 'Recepcion'),
            ('Almacen', 'Almacen'),
            ('Produccion', 'Produccion'),
        ]
    )
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ================ #
#   PROVEEDORES    #
# ================ #
class Proveedores(models.Model):
    id_proveedor = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.TextField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# ========================= #
#     MATERIALES Y FINAL    #
# ========================= #
class Materiales(models.Model):
    id_material = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    punto_reorden = models.IntegerField(validators=[MinValueValidator(0)])
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    critico = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class ProductosTerminados(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    punto_reorden = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nombre

# ========================= #
#    COMPONENTES (Nuevo)    #
# ========================= #
class Componente(models.Model):
    id_componente = models.BigAutoField(primary_key=True)
    material = models.ForeignKey(Materiales, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(ProductosTerminados, on_delete=models.CASCADE, null=True, blank=True)
    
    def clean(self):
        if not (self.material or self.producto):
            raise ValidationError("Debe seleccionar un material o un producto")
        if self.material and self.producto:
            raise ValidationError("Solo puede seleccionar un material O un producto, no ambos")
    
    def __str__(self):
        return f"{self.material or self.producto}"

    @property
    def tipo(self):
        """Propiedad calculada para compatibilidad con código existente"""
        if self.material:
            return 'material'
        if self.producto:
            return 'producto'
        return None

    @property
    def nombre(self):
        """Propiedad para obtener el nombre del componente"""
        return str(self.material or self.producto)

    @property
    def stock_disponible(self):
        """Propiedad para obtener el stock disponible"""
        if self.material:
            return self.material.stock_actual
        if self.producto:
            return self.producto.stock_actual
        return 0

# ========================= #
#    LÍNEAS PRODUCCIÓN     #
# ========================= #
class LineasProduccion(models.Model):
    id_linea = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField(unique=True)
    supervisor = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True, 
                                 limit_choices_to={'rol': 'Produccion'})
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Línea {self.numero} - {self.nombre}"

# ========================= #
#    ORDENES PRODUCCIÓN     #
# ========================= #
class OrdenesProduccion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    id_orden_produccion = models.BigAutoField(primary_key=True)
    codigo_orden = models.CharField(max_length=50, unique=True)
    producto = models.ForeignKey(ProductosTerminados, on_delete=models.PROTECT)
    cantidad_requerida = models.IntegerField(validators=[MinValueValidator(1)])
    cantidad_completada = models.IntegerField(default=0)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendiente')
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.codigo_orden} - {self.producto}"

    def update_status(self):
        if self.estado == 'Cancelada':
            return
        
        total_asignado = self.distribucionlinea_set.aggregate(
            total=models.Sum('cantidad_asignada')
        )['total'] or 0
        
        total_producido = self.distribucionlinea_set.aggregate(
            total=models.Sum('cantidad_producida')
        )['total'] or 0
        
        if total_producido >= self.cantidad_requerida:
            self.estado = 'Completada'
            self.fecha_fin = timezone.now()
        elif total_producido > 0:
            self.estado = 'En Progreso'
        else:
            self.estado = 'Pendiente'
        
        self.cantidad_completada = total_producido
        self.save()

# ========================= #
#  DISTRIBUCIÓN POR LÍNEAS  #
# ========================= #
class DistribucionLinea(models.Model):
    id_distribucion = models.BigAutoField(primary_key=True)
    orden = models.ForeignKey(OrdenesProduccion, on_delete=models.CASCADE)
    linea = models.ForeignKey(LineasProduccion, on_delete=models.PROTECT)
    cantidad_asignada = models.IntegerField(validators=[MinValueValidator(1)])
    cantidad_producida = models.IntegerField(default=0)
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('orden', 'linea')
    
    def __str__(self):
        return f"{self.orden} - {self.linea}"
    
    def save(self, *args, **kwargs):
        if self.cantidad_producida >= self.cantidad_asignada:
            self.completada = True
            if not self.fecha_completada:
                self.fecha_completada = timezone.now()
        else:
            self.completada = False
        
        super().save(*args, **kwargs)
        self.orden.update_status()

# ========================= #
#  REGISTRO PRODUCCIÓN DIARIA
# ========================= #
class RegistroProduccion(models.Model):
    id_registro = models.BigAutoField(primary_key=True)
    distribucion = models.ForeignKey(DistribucionLinea, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    responsable = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar la distribución asociada
        distribucion = self.distribucion
        total_producido = RegistroProduccion.objects.filter(
            distribucion=distribucion
        ).aggregate(
            total=models.Sum('cantidad')
        )['total'] or 0
        
        distribucion.cantidad_producida = total_producido
        distribucion.save()

# ========================= #
#     PEDIDOS PRODUCCIÓN    #
# ========================= #
class PedidoProduccion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
        ('Completado', 'Completado'),
    ]
    id_pedido = models.BigAutoField(primary_key=True)
    orden = models.ForeignKey(OrdenesProduccion, on_delete=models.PROTECT)
    linea = models.ForeignKey(LineasProduccion, on_delete=models.PROTECT)
    componente = models.ForeignKey(Componente, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    aprobado_por = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='pedidos_aprobados')
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.linea}"

# ========================= #
#  ASIGNACIÓN DE MATERIALES #
# ========================= #
class AsignacionMaterial(models.Model):
    id_asignacion = models.BigAutoField(primary_key=True)
    pedido = models.ForeignKey(PedidoProduccion, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cantidad >= self.pedido.cantidad:
            self.pedido.estado = 'Completado'
            self.pedido.save()
    
    def __str__(self):
        return f"Asignación {self.id_asignacion}"

# ========================= #
#        UBICACIONES        #
# ========================= #
class Ubicaciones(models.Model):
    id_ubicacion = models.BigAutoField(primary_key=True)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, null=True, blank=True)
    almacen = models.CharField(max_length=20)
    pasillo = models.CharField(max_length=20, blank=True, null=True)
    rack = models.CharField(max_length=20, blank=True, null=True)
    anaquel = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.almacen}/{self.pasillo or ''}/{self.rack or ''}/{self.anaquel or ''}"

    def clean(self):
        if not self.componente:
            raise ValidationError("Debe asignar un componente a la ubicación")

# ========================= #
#     INVENTARIO ALMACÉN    #
# ========================= #
class InventarioAlmacen(models.Model):
    id_inventario_almacen = models.BigAutoField(primary_key=True)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    ubicacion = models.ForeignKey(Ubicaciones, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_caducidad = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Inventario de Almacén"
        verbose_name_plural = "Inventarios de Almacén"
        unique_together = [['componente', 'ubicacion', 'lote']]

    def __str__(self):
        return f"{self.componente.nombre} - {self.cantidad} unidades"

    def clean(self):
        if self.ubicacion and self.componente != self.ubicacion.componente:
            raise ValidationError("El componente no coincide con la ubicación asignada")

# ======================== #
#    MÓDULO DE RECIBO     #
# ======================== #
class Pedidos(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Recibido', 'Recibido'),
        ('Cancelado', 'Cancelado'),
    ]
    id_pedido = models.BigAutoField(primary_key=True)
    id_material = models.ForeignKey(Materiales, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.id_pedido}"

class EntradasRecibo(models.Model):
    id_recibo = models.BigAutoField(primary_key=True)
    id_material = models.ForeignKey(Materiales, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    factura = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=[('compra', 'Compra'), ('transferencia', 'Transferencia')])
    almacen = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.CharField(max_length=200, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Recibo {self.id_recibo}"

# ======================== #
#      MÓDULO ALMACÉN     #
# ======================== #
class Salidas(models.Model):
    id_salida = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=[('transferencia', 'Transferencia'), ('embarque', 'Embarque')])
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_salida = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Salida {self.id_salida}"

class Mermas(models.Model):
    id_merma = models.BigAutoField(primary_key=True)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_merma = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Merma {self.id_merma}"

# ========================= #
#   NOTIFICACIONES / LOGS   #
# ========================= #
class Notificaciones(models.Model):
    id_notificacion = models.BigAutoField(primary_key=True)
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación {self.id_notificacion}"

class HistorialMovimientos(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
        ('Devolución', 'Devolución'),
        ('Merma', 'Merma'),
    ]
    id_movimiento = models.BigAutoField(primary_key=True)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=50, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Movimiento {self.id_movimiento}"