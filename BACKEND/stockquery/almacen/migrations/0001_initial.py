# Generated by Django 5.0.6 on 2025-03-27 00:43

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LineasProduccion',
            fields=[
                ('id_linea', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('numero', models.IntegerField(unique=True)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Materiales',
            fields=[
                ('id_material', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('punto_reorden', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('stock_actual', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('critico', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenesProduccion',
            fields=[
                ('id_orden_produccion', models.BigAutoField(primary_key=True, serialize=False)),
                ('codigo_orden', models.CharField(max_length=50, unique=True)),
                ('cantidad_requerida', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cantidad_completada', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En Progreso', 'En Progreso'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')], default='Pendiente', max_length=50)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductosTerminados',
            fields=[
                ('id_producto', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('stock_actual', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('punto_reorden', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id_proveedor', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('contacto', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.TextField(blank=True, max_length=20, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id_usuario', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Recepcion', 'Recepcion'), ('Almacen', 'Almacen'), ('Produccion', 'Produccion')], max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('imagen_perfil', models.ImageField(blank=True, null=True, upload_to='perfiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id_componente', models.BigAutoField(primary_key=True, serialize=False)),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.materiales')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.productosterminados')),
            ],
        ),
        migrations.CreateModel(
            name='DistribucionLinea',
            fields=[
                ('id_distribucion', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad_asignada', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cantidad_producida', models.IntegerField(default=0)),
                ('completada', models.BooleanField(default=False)),
                ('fecha_completada', models.DateTimeField(blank=True, null=True)),
                ('linea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.lineasproduccion')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.ordenesproduccion')),
            ],
            options={
                'unique_together': {('orden', 'linea')},
            },
        ),
        migrations.CreateModel(
            name='PedidoProduccion',
            fields=[
                ('id_pedido', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('Completado', 'Completado')], default='Pendiente', max_length=20)),
                ('fecha_aprobacion', models.DateTimeField(blank=True, null=True)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.componente')),
                ('linea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.lineasproduccion')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.ordenesproduccion')),
                ('aprobado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_aprobados', to='almacen.usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='ordenesproduccion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.productosterminados'),
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('id_ubicacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('almacen', models.CharField(max_length=20)),
                ('pasillo', models.CharField(blank=True, max_length=20, null=True)),
                ('rack', models.CharField(blank=True, max_length=20, null=True)),
                ('anaquel', models.CharField(blank=True, max_length=20, null=True)),
                ('componente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.componente')),
            ],
        ),
        migrations.CreateModel(
            name='Salidas',
            fields=[
                ('id_salida', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('transferencia', 'Transferencia'), ('embarque', 'Embarque')], max_length=20)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_salida', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.CharField(max_length=100)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.componente')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroProduccion',
            fields=[
                ('id_registro', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('distribucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.distribucionlinea')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id_pedido', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Recibido', 'Recibido'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20)),
                ('id_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.materiales')),
                ('id_proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.proveedores')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id_notificacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('mensaje', models.TextField()),
                ('fecha_notificacion', models.DateTimeField(auto_now_add=True)),
                ('visto', models.BooleanField(default=False)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Mermas',
            fields=[
                ('id_merma', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_merma', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.CharField(blank=True, max_length=100, null=True)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.componente')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='lineasproduccion',
            name='supervisor',
            field=models.ForeignKey(blank=True, limit_choices_to={'rol': 'Produccion'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='almacen.usuarios'),
        ),
        migrations.CreateModel(
            name='HistorialMovimientos',
            fields=[
                ('id_movimiento', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo_movimiento', models.CharField(choices=[('Entrada', 'Entrada'), ('Salida', 'Salida'), ('Devolución', 'Devolución'), ('Merma', 'Merma')], max_length=50)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_movimiento', models.DateTimeField(auto_now_add=True)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.componente')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='EntradasRecibo',
            fields=[
                ('id_recibo', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('lote', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_serie', models.CharField(blank=True, max_length=100, null=True)),
                ('factura', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('compra', 'Compra'), ('transferencia', 'Transferencia')], max_length=20)),
                ('almacen', models.CharField(blank=True, max_length=100, null=True)),
                ('qr_code', models.CharField(blank=True, max_length=200, null=True)),
                ('id_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.materiales')),
                ('id_proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacen.proveedores')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionMaterial',
            fields=[
                ('id_asignacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.pedidoproduccion')),
                ('asignado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='almacen.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='InventarioAlmacen',
            fields=[
                ('id_inventario_almacen', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('lote', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_caducidad', models.DateField(blank=True, null=True)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.componente')),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='almacen.ubicaciones')),
            ],
            options={
                'verbose_name': 'Inventario de Almacén',
                'verbose_name_plural': 'Inventarios de Almacén',
                'unique_together': {('componente', 'ubicacion', 'lote')},
            },
        ),
    ]
