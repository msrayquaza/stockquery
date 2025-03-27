import os
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockquery.settings')
import django
django.setup()

from django.contrib.auth.hashers import make_password
from almacen.models import (
    Usuarios, Proveedores, Materiales, ProductosTerminados, Componente,
    LineasProduccion, OrdenesProduccion, DistribucionLinea, RegistroProduccion,
    PedidoProduccion, AsignacionMaterial, Ubicaciones, InventarioAlmacen,
    Pedidos, EntradasRecibo, Salidas, Mermas, Notificaciones, HistorialMovimientos
)

# Configuración inicial
NUM_USUARIOS = 10
NUM_PROVEEDORES = 5
NUM_MATERIALES = 15
NUM_PRODUCTOS = 8
NUM_LINEAS = 3
NUM_ORDENES = 12
NUM_PEDIDOS = 20
NUM_ENTRADAS = 30
NUM_SALIDAS = 25
NUM_MERMAS = 10
NUM_NOTIFICACIONES = 15

# Imágenes de ejemplo (debes tener estas imágenes en tu media folder)
IMAGENES_PERFIL = [
    'perfiles/user1.jpg',
    'perfiles/user2.jpg',
    'perfiles/user3.jpg',
]

def create_usuarios():
    print("Creando usuarios...")
    roles = ['Administrador', 'Recepcion', 'Almacen', 'Produccion']
    nombres = ['Juan', 'Maria', 'Carlos', 'Laura', 'Pedro', 'Ana', 'Luis', 'Sofia', 'Diego', 'Elena']
    apellidos = ['Gomez', 'Lopez', 'Martinez', 'Rodriguez', 'Perez', 'Garcia', 'Sanchez', 'Diaz', 'Fernandez', 'Torres']
    
    # Crear superusuario
    Usuarios.objects.get_or_create(
        nombre='Admin',
        apellido='Sistema',
        correo='admin@empresa.com',
        defaults={
            'contraseña': make_password('admin123'),
            'rol': 'Administrador',
            'activo': True
        }
    )
    
    for i in range(NUM_USUARIOS):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        # Asegurar que el correo sea único añadiendo un número si es necesario
        base_correo = f"{nombre.lower()}.{apellido.lower()}@empresa.com"
        correo = base_correo
        counter = 1
        while Usuarios.objects.filter(correo=correo).exists():
            correo = f"{nombre.lower()}.{apellido.lower()}{counter}@empresa.com"
            counter += 1
            
        Usuarios.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=make_password('password123'),
            rol=random.choice(roles),
            activo=random.choice([True, False]),
            # imagen_perfil=File(open(random.choice(IMAGENES_PERFIL), 'rb')) if i < 3 else None
        )

def create_proveedores():
    print("Creando proveedores...")
    nombres = ['MateriasPrimas S.A.', 'Suministros Industriales', 'TecnoMateriales', 
               'Global Components', 'Distribuidora Nacional']
    contactos = ['Juan Perez', 'Maria Gomez', 'Carlos Ruiz', 'Laura Diaz', 'Pedro Martinez']
    
    for i in range(NUM_PROVEEDORES):
        Proveedores.objects.create(
            nombre=nombres[i],
            contacto=contactos[i],
            telefono=f"555-{random.randint(1000,9999)}",
            correo=f"contacto@{nombres[i].replace(' ', '').lower()}.com",
            direccion=f"Calle {random.randint(1,100)}, Ciudad {i+1}"
        )

def create_materiales():
    print("Creando materiales...")
    materiales = [
        ('Acero inoxidable', 'kg'), ('Plástico ABS', 'kg'), ('Tornillos 5mm', 'unidad'),
        ('Pintura blanca', 'litro'), ('Vidrio templado', 'm2'), ('Aluminio', 'kg'),
        ('Cables eléctricos', 'm'), ('Circuitos impresos', 'unidad'), ('Silicona', 'litro'),
        ('Madera contrachapada', 'm2'), ('Tela impermeable', 'm2'), ('Goma espuma', 'm2'),
        ('Pegamento industrial', 'litro'), ('Tornillos 3mm', 'unidad'), ('Poliuretano', 'kg')
    ]
    
    for nombre, unidad in materiales:
        punto_reorden = random.randint(50, 200)
        stock = random.randint(0, 300)
        Materiales.objects.create(
            nombre=nombre,
            descripcion=f"Material {nombre} para producción",
            punto_reorden=punto_reorden,
            stock_actual=stock,
            critico=stock < punto_reorden
        )

def create_productos_terminados():
    print("Creando productos terminados...")
    productos = [
        ('Silla ergonómica', 'Silla de oficina con ajustes'),
        ('Mesa de reuniones', 'Mesa para 8 personas'),
        ('Estantería modular', 'Estantería de 5 niveles'),
        ('Escritorio ejecutivo', 'Escritorio de madera maciza'),
        ('Lámpara LED', 'Lámpara de techo 50W'),
        ('Sofá ejecutivo', 'Sofá de piel sintética'),
        ('Archivador metálico', 'Archivador de 4 cajones'),
        ('Panel divisorio', 'Panel acústico para oficinas')
    ]
    
    for nombre, descripcion in productos:
        punto_reorden = random.randint(5, 20)
        stock = random.randint(0, 50)
        ProductosTerminados.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            stock_actual=stock,
            punto_reorden=punto_reorden
        )

def create_componentes():
    print("Creando componentes...")
    materiales = Materiales.objects.all()
    productos = ProductosTerminados.objects.all()
    
    # Crear componentes para materiales
    for material in materiales:
        Componente.objects.create(material=material)
    
    # Crear componentes para productos
    for producto in productos:
        Componente.objects.create(producto=producto)

def create_lineas_produccion():
    print("Creando líneas de producción...")
    nombres = ['Ensamblado', 'Acabados', 'Pintura']
    supervisores = Usuarios.objects.filter(rol='Produccion')
    
    for i in range(NUM_LINEAS):
        LineasProduccion.objects.create(
            nombre=nombres[i],
            numero=i+1,
            supervisor=random.choice(supervisores) if supervisores.exists() else None,
            activa=random.choice([True, False]) if i > 0 else True  # La primera siempre activa
        )

def create_ordenes_produccion():
    print("Creando órdenes de producción...")
    estados = ['Pendiente', 'En Progreso', 'Completada', 'Cancelada']
    productos = ProductosTerminados.objects.all()
    usuarios = Usuarios.objects.all()
    
    for i in range(NUM_ORDENES):
        producto = random.choice(productos)
        fecha_inicio = timezone.now() - timedelta(days=random.randint(1, 60))
        estado = random.choice(estados)
        
        orden = OrdenesProduccion.objects.create(
            codigo_orden=f"ORD-{1000+i}",
            producto=producto,
            cantidad_requerida=random.randint(10, 100),
            cantidad_completada=0 if estado == 'Pendiente' else random.randint(5, 100),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio + timedelta(days=random.randint(1, 10)) if estado in ['Completada', 'Cancelada'] else None,
            estado=estado,
            descripcion=f"Orden para producir {producto.nombre}"
        )
        
        # Actualizar cantidad completada si es necesario
        if estado == 'Completada':
            orden.cantidad_completada = orden.cantidad_requerida
            orden.save()

def create_distribucion_linea():
    print("Creando distribuciones por línea...")
    ordenes = OrdenesProduccion.objects.all()
    lineas = LineasProduccion.objects.all()
    
    for orden in ordenes:
        for linea in lineas:
            if random.choice([True, False]):  # 50% de probabilidad de asignar a cada línea
                cantidad_asignada = random.randint(1, orden.cantidad_requerida // len(lineas))
                cantidad_producida = random.randint(0, cantidad_asignada) if orden.estado != 'Pendiente' else 0
                
                DistribucionLinea.objects.create(
                    orden=orden,
                    linea=linea,
                    cantidad_asignada=cantidad_asignada,
                    cantidad_producida=cantidad_producida,
                    completada=cantidad_producida >= cantidad_asignada,
                    fecha_completada=timezone.now() - timedelta(days=random.randint(1, 5)) if cantidad_producida >= cantidad_asignada else None
                )

def create_registro_produccion():
    print("Creando registros de producción...")
    distribuciones = DistribucionLinea.objects.filter(orden__estado__in=['En Progreso', 'Completada'])
    usuarios = Usuarios.objects.filter(rol='Produccion')
    
    for distribucion in distribuciones:
        num_registros = random.randint(1, 5)
        for _ in range(num_registros):
            fecha = distribucion.orden.fecha_inicio + timedelta(days=random.randint(0, 5))
            RegistroProduccion.objects.create(
                distribucion=distribucion,
                fecha=fecha,
                cantidad=random.randint(1, distribucion.cantidad_asignada // 2),
                responsable=random.choice(usuarios),
                observaciones=f"Registro de producción para {distribucion.linea.nombre}"
            )

def create_pedidos_produccion():
    print("Creando pedidos de producción...")
    ordenes = OrdenesProduccion.objects.all()
    lineas = LineasProduccion.objects.all()
    componentes = Componente.objects.all()
    estados = ['Pendiente', 'Aprobado', 'Rechazado', 'Completado']
    usuarios = Usuarios.objects.filter(rol='Produccion')
    
    for i in range(NUM_PEDIDOS):
        orden = random.choice(ordenes)
        linea = random.choice(lineas)
        componente = random.choice(componentes)
        estado = random.choice(estados)
        
        pedido = PedidoProduccion.objects.create(
            orden=orden,
            linea=linea,
            componente=componente,
            cantidad=random.randint(1, 100),
            estado=estado,
            aprobado_por=random.choice(usuarios) if estado in ['Aprobado', 'Completado'] else None,
            fecha_aprobacion=timezone.now() - timedelta(days=random.randint(1, 3)) if estado in ['Aprobado', 'Completado'] else None
        )
        
        # Crear asignación de materiales si el pedido está completado
        if estado == 'Completado':
            AsignacionMaterial.objects.create(
                pedido=pedido,
                cantidad=pedido.cantidad,
                asignado_por=random.choice(usuarios)
            )

def create_ubicaciones():
    print("Creando ubicaciones...")
    componentes = Componente.objects.all()
    almacenes = ['Principal', 'Secundario', 'Materias Primas']
    
    for componente in componentes:
        for i in range(random.randint(1, 2)):  # 1-2 ubicaciones por componente
            Ubicaciones.objects.create(
                componente=componente,
                almacen=random.choice(almacenes),
                pasillo=f"P{random.randint(1, 10)}",
                rack=f"R{random.randint(1, 5)}",
                anaquel=f"A{random.randint(1, 3)}"
            )

def create_inventario_almacen():
    print("Creando inventario de almacén...")
    componentes = Componente.objects.all()
    ubicaciones = Ubicaciones.objects.all()
    
    for componente in componentes:
        ubicacion = random.choice(ubicaciones.filter(componente=componente))
        InventarioAlmacen.objects.create(
            componente=componente,
            cantidad=random.randint(10, 100),
            ubicacion=ubicacion,
            lote=f"LOTE-{random.randint(1000, 9999)}",
            fecha_caducidad=timezone.now() + timedelta(days=random.randint(30, 365)) if random.choice([True, False]) else None
        )

def create_pedidos():
    print("Creando pedidos...")
    materiales = Materiales.objects.all()
    proveedores = Proveedores.objects.all()
    usuarios = Usuarios.objects.filter(rol__in=['Recepcion', 'Almacen'])
    estados = ['Pendiente', 'En Proceso', 'Recibido', 'Cancelado']
    
    for i in range(NUM_PEDIDOS):
        Pedidos.objects.create(
            id_material=random.choice(materiales),
            id_proveedor=random.choice(proveedores),
            cantidad=random.randint(10, 100),
            estado=random.choice(estados),
            id_usuario=random.choice(usuarios)
        )

def create_entradas_recibo():
    print("Creando entradas de recibo...")
    pedidos = Pedidos.objects.filter(estado='Recibido')
    materiales = Materiales.objects.all()
    proveedores = Proveedores.objects.all()
    usuarios = Usuarios.objects.filter(rol__in=['Recepcion', 'Almacen'])
    
    for i in range(NUM_ENTRADAS):
        material = random.choice(materiales)
        EntradasRecibo.objects.create(
            id_material=material,
            id_proveedor=random.choice(proveedores),
            cantidad=random.randint(5, 50),
            lote=f"LOTE-{random.randint(1000, 9999)}",
            numero_serie=f"SN-{random.randint(10000, 99999)}" if random.choice([True, False]) else None,
            factura=f"FACT-{random.randint(100, 999)}",
            tipo=random.choice(['compra', 'transferencia']),
            almacen=random.choice(['Principal', 'Secundario']),
            id_usuario=random.choice(usuarios)
        )
        
        # Actualizar stock del material
        material.stock_actual += random.randint(5, 50)
        material.save()

def create_salidas():
    print("Creando salidas...")
    componentes = Componente.objects.all()
    usuarios = Usuarios.objects.filter(rol__in=['Almacen', 'Produccion'])
    
    for i in range(NUM_SALIDAS):
        componente = random.choice(componentes)
        Salidas.objects.create(
            tipo=random.choice(['transferencia', 'embarque']),
            componente=componente,
            cantidad=random.randint(1, 20),
            motivo=random.choice(['Producción', 'Venta', 'Transferencia entre almacenes']),
            id_usuario=random.choice(usuarios)
        )
        
        # Actualizar stock del componente
        if componente.material:
            componente.material.stock_actual = max(0, componente.material.stock_actual - random.randint(1, 20))
            componente.material.save()
        elif componente.producto:
            componente.producto.stock_actual = max(0, componente.producto.stock_actual - random.randint(1, 20))
            componente.producto.save()

def create_mermas():
    print("Creando mermas...")
    componentes = Componente.objects.all()
    usuarios = Usuarios.objects.filter(rol__in=['Almacen', 'Produccion'])
    
    for i in range(NUM_MERMAS):
        componente = random.choice(componentes)
        Mermas.objects.create(
            componente=componente,
            cantidad=random.randint(1, 5),
            motivo=random.choice(['Dañado', 'Caducado', 'Error de producción']),
            id_usuario=random.choice(usuarios)
        )
        
        # Actualizar stock del componente
        if componente.material:
            componente.material.stock_actual = max(0, componente.material.stock_actual - random.randint(1, 5))
            componente.material.save()
        elif componente.producto:
            componente.producto.stock_actual = max(0, componente.producto.stock_actual - random.randint(1, 5))
            componente.producto.save()

def create_notificaciones():
    print("Creando notificaciones...")
    usuarios = Usuarios.objects.all()
    mensajes = [
        'Nueva orden de producción creada',
        'Material crítico bajo stock',
        'Pedido recibido',
        'Producción completada',
        'Error en línea de producción'
    ]
    
    for i in range(NUM_NOTIFICACIONES):
        Notificaciones.objects.create(
            mensaje=random.choice(mensajes),
            id_usuario=random.choice(usuarios),
            visto=random.choice([True, False])
        )

def create_historial_movimientos():
    print("Creando historial de movimientos...")
    componentes = Componente.objects.all()
    usuarios = Usuarios.objects.all()
    tipos = ['Entrada', 'Salida', 'Devolución', 'Merma']
    
    for i in range(50):  # Más movimientos para mejor análisis
        componente = random.choice(componentes)
        tipo = random.choice(tipos)
        cantidad = random.randint(1, 20)
        
        HistorialMovimientos.objects.create(
            componente=componente,
            tipo_movimiento=tipo,
            cantidad=cantidad,
            id_usuario=random.choice(usuarios)
        )

def main():
    print("Iniciando población de la base de datos...")
    
    # Limpiar base de datos (opcional, cuidado en producción)
    print("Limpiando base de datos...")
    for model in [Usuarios, Proveedores, Materiales, ProductosTerminados, Componente,
                  LineasProduccion, OrdenesProduccion, DistribucionLinea, RegistroProduccion,
                  PedidoProduccion, AsignacionMaterial, Ubicaciones, InventarioAlmacen,
                  Pedidos, EntradasRecibo, Salidas, Mermas, Notificaciones, HistorialMovimientos]:
        model.objects.all().delete()
    
    # Crear datos en el orden correcto para respetar relaciones
    create_usuarios()
    create_proveedores()
    create_materiales()
    create_productos_terminados()
    create_componentes()
    create_lineas_produccion()
    create_ordenes_produccion()
    create_distribucion_linea()
    create_registro_produccion()
    create_pedidos_produccion()
    create_ubicaciones()
    create_inventario_almacen()
    create_pedidos()
    create_entradas_recibo()
    create_salidas()
    create_mermas()
    create_notificaciones()
    create_historial_movimientos()
    
    print("¡Base de datos poblada exitosamente!")

if __name__ == '__main__':
    main()