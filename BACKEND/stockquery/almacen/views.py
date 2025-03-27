from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Usuarios, Proveedores, Materiales, ProductosTerminados, OrdenesProduccion,
    AsignacionMaterial, Pedidos, EntradasRecibo, Salidas, Mermas, 
    Ubicaciones, InventarioAlmacen, Notificaciones, HistorialMovimientos,
    LineasProduccion, DistribucionLinea, RegistroProduccion, PedidoProduccion,
    Componente
)
from .serializers import (
    UsuariosSerializer, ProveedoresSerializer, MaterialesSerializer,
    ProductosTerminadosSerializer, OrdenesProduccionSerializer,
    AsignacionMaterialSerializer, UbicacionesSerializer, 
    EntradasReciboSerializer, SalidasSerializer, InventarioAlmacenSerializer,
    MermasSerializer, NotificacionesSerializer, HistorialMovimientosSerializer,
    RegisterSerializer, LoginSerializer, LineasProduccionSerializer,
    DistribucionLineaSerializer, RegistroProduccionSerializer,
    PedidoProduccionSerializer, ComponenteSerializer, PedidosSerializer
)

# ==========================
#   VISTAS DE AUTENTICACIÓN
# ==========================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {
                    "message": "Usuario registrado con éxito",
                    "usuario": {
                        "id_usuario": usuario.id_usuario,
                        "nombre": usuario.nombre,
                        "correo": usuario.correo,
                        "rol": usuario.rol,
                        "activo": usuario.activo
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        correo = data.get("correo")
        contraseña = data.get("contraseña")

        try:
            usuario = Usuarios.objects.get(correo=correo)

            if usuario and usuario.contraseña == contraseña:
                request.session["usuario_id"] = usuario.id_usuario
                request.session.save()

                response = Response({
                    "mensaje": "Login exitoso",
                    "usuario": {
                        "id_usuario": usuario.id_usuario,
                        "nombre": usuario.nombre,
                        "correo": usuario.correo,
                        "rol": usuario.rol,
                    }
                })

                response.set_cookie(
                    key="sessionid",
                    value=request.session.session_key,
                    httponly=True,
                    secure=True,
                    samesite="Lax"
                )
                return response
            else:
                return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        except Usuarios.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        response = Response({"mensaje": "Sesión cerrada"}, status=status.HTTP_200_OK)
        response.delete_cookie("sessionid")
        return response

class UsuarioInfoView(APIView):
    def get(self, request):
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            usuario = Usuarios.objects.get(id_usuario=usuario_id)
            imagen_perfil_url = (
                request.build_absolute_uri(usuario.imagen_perfil.url)
                if usuario.imagen_perfil
                else None
            )
            return Response({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "imagen_perfil": imagen_perfil_url,
            })
        except Usuarios.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# ============================
#     VISTAS MODELVIEWSET
# ============================
class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'apellido', 'correo', 'rol', 'activo']

class ProveedoresViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'correo', 'telefono']

class MaterialesViewSet(viewsets.ModelViewSet):
    queryset = Materiales.objects.all()
    serializer_class = MaterialesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class ProductosTerminadosViewSet(viewsets.ModelViewSet):
    queryset = ProductosTerminados.objects.all()
    serializer_class = ProductosTerminadosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'stock_actual', 'punto_reorden']

class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['material', 'producto']

class LineasProduccionViewSet(viewsets.ModelViewSet):
    queryset = LineasProduccion.objects.all()
    serializer_class = LineasProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'numero', 'activa']

class OrdenesProduccionViewSet(viewsets.ModelViewSet):
    queryset = OrdenesProduccion.objects.all()
    serializer_class = OrdenesProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo_orden', 'estado', 'fecha_inicio', 'fecha_fin']

class DistribucionLineaViewSet(viewsets.ModelViewSet):
    queryset = DistribucionLinea.objects.all()
    serializer_class = DistribucionLineaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['orden', 'linea', 'completada']

class RegistroProduccionViewSet(viewsets.ModelViewSet):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['distribucion', 'fecha', 'responsable']

class PedidoProduccionViewSet(viewsets.ModelViewSet):
    queryset = PedidoProduccion.objects.all()
    serializer_class = PedidoProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['orden', 'linea', 'componente', 'estado']

class AsignacionMaterialViewSet(viewsets.ModelViewSet):
    queryset = AsignacionMaterial.objects.all()
    serializer_class = AsignacionMaterialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pedido', 'asignado_por']

class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'id_material', 'id_proveedor', 'id_usuario', 'fecha_pedido']

class EntradasReciboViewSet(viewsets.ModelViewSet):
    queryset = EntradasRecibo.objects.all()
    serializer_class = EntradasReciboSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_material', 'id_proveedor', 'id_usuario', 'fecha_entrada']

class SalidasViewSet(viewsets.ModelViewSet):
    queryset = Salidas.objects.all()
    serializer_class = SalidasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['componente', 'tipo', 'id_usuario', 'fecha_salida']

class MermasViewSet(viewsets.ModelViewSet):
    queryset = Mermas.objects.all()
    serializer_class = MermasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['componente', 'id_usuario', 'fecha_merma']

class UbicacionesViewSet(viewsets.ModelViewSet):
    queryset = Ubicaciones.objects.all()
    serializer_class = UbicacionesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['componente', 'almacen', 'pasillo', 'rack', 'anaquel']

class InventarioAlmacenViewSet(viewsets.ModelViewSet):
    queryset = InventarioAlmacen.objects.all()
    serializer_class = InventarioAlmacenSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['componente', 'ubicacion', 'fecha_actualizacion']

class NotificacionesViewSet(viewsets.ModelViewSet):
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_usuario', 'visto', 'fecha_notificacion']

class HistorialMovimientosViewSet(viewsets.ModelViewSet):
    queryset = HistorialMovimientos.objects.all()
    serializer_class = HistorialMovimientosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['componente', 'tipo_movimiento', 'fecha_movimiento', 'id_usuario']