from django.contrib import admin
from .models import (
    Usuarios, Proveedores, Materiales, ProductosTerminados,
    OrdenesProduccion, AsignacionMaterial, Ubicaciones, EntradasRecibo, 
    Salidas, InventarioAlmacen, Mermas, Notificaciones, 
    HistorialMovimientos, Componente, LineasProduccion,
    DistribucionLinea, RegistroProduccion, PedidoProduccion
)

# Clases personalizadas para modelos importantes
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'correo', 'rol', 'activo')
    list_filter = ('rol', 'activo')
    search_fields = ('nombre', 'apellido', 'correo')
    ordering = ('nombre', 'apellido')

class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre', 'contacto', 'telefono', 'correo')
    search_fields = ('nombre', 'contacto', 'correo')
    list_filter = ('nombre',)

class MaterialesAdmin(admin.ModelAdmin):
    list_display = ('id_material', 'nombre', 'stock_actual', 'punto_reorden', 'critico')
    list_filter = ('critico',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

class ProductosTerminadosAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'stock_actual', 'punto_reorden')
    search_fields = ('nombre',)
    ordering = ('nombre',)

class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('id_componente', 'get_nombre', 'get_tipo', 'stock_disponible')
    list_filter = ('material', 'producto')
    search_fields = ('material__nombre', 'producto__nombre')
    
    def get_nombre(self, obj):
        return obj.nombre
    get_nombre.short_description = 'Nombre'
    
    def get_tipo(self, obj):
        return obj.tipo
    get_tipo.short_description = 'Tipo'

class OrdenesProduccionAdmin(admin.ModelAdmin):
    list_display = ('codigo_orden', 'producto', 'cantidad_requerida', 'cantidad_completada', 'estado', 'fecha_inicio')
    list_filter = ('estado', 'producto')
    search_fields = ('codigo_orden', 'producto__nombre')
    date_hierarchy = 'fecha_inicio'

class LineasProduccionAdmin(admin.ModelAdmin):
    list_display = ('id_linea', 'nombre', 'numero', 'supervisor', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'numero')
    raw_id_fields = ('supervisor',)

class DistribucionLineaAdmin(admin.ModelAdmin):
    list_display = ('id_distribucion', 'orden', 'linea', 'cantidad_asignada', 'cantidad_producida', 'completada')
    list_filter = ('completada', 'linea')
    search_fields = ('orden__codigo_orden', 'linea__nombre')

class PedidoProduccionAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'orden', 'linea', 'componente', 'cantidad', 'estado')
    list_filter = ('estado', 'linea')
    search_fields = ('orden__codigo_orden', 'componente__nombre')

class InventarioAlmacenAdmin(admin.ModelAdmin):
    list_display = ('id_inventario_almacen', 'componente', 'cantidad', 'ubicacion', 'fecha_actualizacion')
    list_filter = ('ubicacion',)
    search_fields = ('componente__nombre', 'ubicacion__almacen')
    date_hierarchy = 'fecha_actualizacion'

class HistorialMovimientosAdmin(admin.ModelAdmin):
    list_display = ('id_movimiento', 'componente', 'tipo_movimiento', 'cantidad', 'fecha_movimiento', 'id_usuario')
    list_filter = ('tipo_movimiento',)
    search_fields = ('componente__nombre', 'id_usuario__nombre')
    date_hierarchy = 'fecha_movimiento'

# Registro de modelos con sus clases personalizadas
admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Proveedores, ProveedoresAdmin)
admin.site.register(Materiales, MaterialesAdmin)
admin.site.register(ProductosTerminados, ProductosTerminadosAdmin)
admin.site.register(Componente, ComponenteAdmin)
admin.site.register(OrdenesProduccion, OrdenesProduccionAdmin)
admin.site.register(LineasProduccion, LineasProduccionAdmin)
admin.site.register(DistribucionLinea, DistribucionLineaAdmin)
admin.site.register(RegistroProduccion)
admin.site.register(PedidoProduccion, PedidoProduccionAdmin)
admin.site.register(AsignacionMaterial)
admin.site.register(Ubicaciones)
admin.site.register(EntradasRecibo)
admin.site.register(Salidas)
admin.site.register(InventarioAlmacen, InventarioAlmacenAdmin)
admin.site.register(Mermas)
admin.site.register(Notificaciones)
admin.site.register(HistorialMovimientos, HistorialMovimientosAdmin)

# Modelos eliminados comentados para referencia:
# admin.site.register(Transferencias)
# admin.site.register(AjustesInventario)
# admin.site.register(Facturas)
# admin.site.register(DetallesFactura)
# admin.site.register(Inspecciones)