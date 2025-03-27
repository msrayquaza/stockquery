from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # ModelViewSets
    UsuariosViewSet,
    ProveedoresViewSet,
    MaterialesViewSet,
    ProductosTerminadosViewSet,
    ComponenteViewSet,
    LineasProduccionViewSet,
    OrdenesProduccionViewSet,
    DistribucionLineaViewSet,
    RegistroProduccionViewSet,
    PedidoProduccionViewSet,
    AsignacionMaterialViewSet,
    UbicacionesViewSet,
    PedidosViewSet,
    EntradasReciboViewSet,
    SalidasViewSet,
    MermasViewSet,
    InventarioAlmacenViewSet,
    NotificacionesViewSet,
    HistorialMovimientosViewSet,

    # Autenticación / APIView
    RegisterView,
    LoginView,
    LogoutView,
    UsuarioInfoView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuariosViewSet)
router.register(r'proveedores', ProveedoresViewSet)
router.register(r'materiales', MaterialesViewSet)
router.register(r'productos-terminados', ProductosTerminadosViewSet)
router.register(r'componentes', ComponenteViewSet)
router.register(r'lineas-produccion', LineasProduccionViewSet)
router.register(r'ordenes-produccion', OrdenesProduccionViewSet)
router.register(r'distribucion-linea', DistribucionLineaViewSet)
router.register(r'registro-produccion', RegistroProduccionViewSet)
router.register(r'pedido-produccion', PedidoProduccionViewSet)
router.register(r'asignacion-material', AsignacionMaterialViewSet)
router.register(r'ubicaciones', UbicacionesViewSet)
router.register(r'pedidos', PedidosViewSet)
router.register(r'entradas-recibo', EntradasReciboViewSet)
router.register(r'salidas', SalidasViewSet)
router.register(r'mermas', MermasViewSet)
router.register(r'inventario-almacen', InventarioAlmacenViewSet)
router.register(r'notificaciones', NotificacionesViewSet)
router.register(r'historial-movimientos', HistorialMovimientosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuario_info/', UsuarioInfoView.as_view(), name='usuario_info'),
]
    