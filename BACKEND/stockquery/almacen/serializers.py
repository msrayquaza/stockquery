from rest_framework import serializers
from .models import (
    Usuarios, Proveedores, Materiales, ProductosTerminados, OrdenesProduccion,
    AsignacionMaterial, Pedidos, EntradasRecibo, Salidas, Mermas, 
    Ubicaciones, InventarioAlmacen, Notificaciones, HistorialMovimientos,
    LineasProduccion, DistribucionLinea, RegistroProduccion, PedidoProduccion,
    Componente
)

## SERIALIZERS LOGIN
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = [
            'id_usuario', 'nombre', 'apellido', 'correo',
            'contraseña', 'rol', 'activo', 'imagen_perfil'
        ]
        extra_kwargs = {
            'contraseña': {'write_only': True},
            'imagen_perfil': {'required': False}
        }

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    contraseña = serializers.CharField(write_only=True)

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = [
            'id_usuario', 'nombre', 'apellido', 'correo', 'contraseña',
            'rol', 'activo', 'fecha_registro', 'imagen_perfil'
        ]
        extra_kwargs = {
            'contraseña': {'write_only': True}
        }

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = '__all__'

class MaterialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiales
        fields = '__all__'

class ProductosTerminadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosTerminados
        fields = '__all__'

class ComponenteSerializer(serializers.ModelSerializer):
    material = MaterialesSerializer(read_only=True)
    producto = ProductosTerminadosSerializer(read_only=True)
    
    class Meta:
        model = Componente
        fields = '__all__'

class LineasProduccionSerializer(serializers.ModelSerializer):
    supervisor = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = LineasProduccion
        fields = '__all__'

class OrdenesProduccionSerializer(serializers.ModelSerializer):
    producto = ProductosTerminadosSerializer(read_only=True)
    
    class Meta:
        model = OrdenesProduccion
        fields = '__all__'

class DistribucionLineaSerializer(serializers.ModelSerializer):
    orden = OrdenesProduccionSerializer(read_only=True)
    linea = LineasProduccionSerializer(read_only=True)
    
    class Meta:
        model = DistribucionLinea
        fields = '__all__'

class RegistroProduccionSerializer(serializers.ModelSerializer):
    distribucion = DistribucionLineaSerializer(read_only=True)
    responsable = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = RegistroProduccion
        fields = '__all__'

class PedidoProduccionSerializer(serializers.ModelSerializer):
    orden = OrdenesProduccionSerializer(read_only=True)
    linea = LineasProduccionSerializer(read_only=True)
    componente = ComponenteSerializer(read_only=True)
    aprobado_por = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = PedidoProduccion
        fields = '__all__'

class AsignacionMaterialSerializer(serializers.ModelSerializer):
    pedido = PedidoProduccionSerializer(read_only=True)
    asignado_por = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = AsignacionMaterial
        fields = '__all__'

class UbicacionesSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    
    class Meta:
        model = Ubicaciones
        fields = '__all__'

class PedidosSerializer(serializers.ModelSerializer):
    id_material = MaterialesSerializer(read_only=True)
    id_proveedor = ProveedoresSerializer(read_only=True)
    id_usuario = UsuariosSerializer(read_only=True)

    class Meta:
        model = Pedidos
        fields = '__all__'

class EntradasReciboSerializer(serializers.ModelSerializer):
    id_material = MaterialesSerializer(read_only=True)
    id_proveedor = ProveedoresSerializer(read_only=True)
    id_usuario = UsuariosSerializer(read_only=True)

    class Meta:
        model = EntradasRecibo
        fields = '__all__'

class SalidasSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    id_usuario = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = Salidas
        fields = '__all__'

class MermasSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    id_usuario = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = Mermas
        fields = '__all__'

class InventarioAlmacenSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    ubicacion = UbicacionesSerializer(read_only=True)
    
    class Meta:
        model = InventarioAlmacen
        fields = '__all__'

class NotificacionesSerializer(serializers.ModelSerializer):
    id_usuario = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = Notificaciones
        fields = '__all__'

class HistorialMovimientosSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    id_usuario = UsuariosSerializer(read_only=True)
    
    class Meta:
        model = HistorialMovimientos
        fields = '__all__'