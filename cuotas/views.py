from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from .forms import PagoCuotaForm
import random
import json
import logging

# Configurar logger para esta vista
logger = logging.getLogger(__name__)

def lista_pagos(request):
    # Mostrar cuotas y pagos reales desde la base de datos
    from .models import CuotaEstudiante, PagoCuota
    cuotas = CuotaEstudiante.objects.select_related('estudiante', 'actividad', 'estudiante__curso').all()

    # Filtros (RF-04: Filtrar cuotas por nombre, RUT, actividad)
    estudiante_filtro = request.GET.get('estudiante', '')
    rut_filtro = request.GET.get('rut', '')
    actividad_filtro = request.GET.get('actividad', '')
    estado_filtro = request.GET.get('estado', '')

    if estudiante_filtro:
        cuotas = cuotas.filter(estudiante__nombre__icontains=estudiante_filtro)
    if rut_filtro:
        cuotas = cuotas.filter(estudiante__rut__icontains=rut_filtro)
    if actividad_filtro:
        cuotas = cuotas.filter(actividad__nombre__icontains=actividad_filtro)
    if estado_filtro:
        cuotas = cuotas.filter(estado__icontains=estado_filtro)

    pagos = []
    for cuota in cuotas:
        ultimo_pago = PagoCuota.objects.filter(cuota=cuota).order_by('-fecha_pago').first()
        pagos.append({
            'id': cuota.id,
            'estudiante': f"{cuota.estudiante.nombre} {cuota.estudiante.apellido_paterno} {cuota.estudiante.apellido_materno}",
            'rut_estudiante': cuota.estudiante.rut,
            'curso': str(cuota.estudiante.curso),
            'actividad': cuota.actividad.nombre,
            'monto_total': cuota.monto_total,
            'monto_pagado': cuota.monto_pagado,
            'saldo_pendiente': cuota.saldo_pendiente(),
            'estado': cuota.estado.capitalize(),
            'fecha_vencimiento': cuota.fecha_vencimiento.strftime('%Y-%m-%d'),
            'ultimo_pago': ultimo_pago.fecha_pago.strftime('%Y-%m-%d') if ultimo_pago else None,
            'metodo_pago': ultimo_pago.metodo_pago.capitalize() if ultimo_pago else None
        })

    context = {
        'pagos': pagos,
        'filtros': {
            'estudiante': estudiante_filtro,
            'rut': rut_filtro,
            'actividad': actividad_filtro,
            'estado': estado_filtro,
        }
    }

    return render(request, 'cuotas/lista_pagos.html', context)

def registrar_pago(request):
    logger.info(f"🔥 Iniciando registrar_pago - Método: {request.method}")
    
    if request.method == 'POST':
        logger.info(f"📝 Datos POST recibidos: {dict(request.POST)}")
        form = PagoCuotaForm(request.POST)
        
        if not form.is_valid():
            logger.error(f"❌ Formulario inválido - Errores: {form.errors}")
            messages.error(request, 'Por favor corrija los errores en el formulario.')
        else:
            logger.info("✅ Formulario válido, procesando datos...")
            try:
                monto = form.cleaned_data['monto']
                metodo = form.cleaned_data['metodo_pago']
                observacion = form.cleaned_data['observacion']
                
                logger.info(f"💰 Datos del pago - Monto: {monto}, Método: {metodo}, Obs: {observacion}")
                
                # Obtener datos del formulario
                estudiante_id = request.POST.get('estudiante')
                actividad_nombre = request.POST.get('actividad')
                
                logger.info(f"🎓 Buscando - Estudiante ID: {estudiante_id}, Actividad: {actividad_nombre}")
                
                # Buscar el estudiante y la actividad
                from estudiantes.models import Estudiante
                from actividades.models import Actividad
                from .models import CuotaEstudiante, PagoCuota
                
                estudiante = Estudiante.objects.get(id=estudiante_id)
                logger.info(f"✅ Estudiante encontrado: {estudiante}")
                
                actividad = Actividad.objects.get(nombre=actividad_nombre)
                logger.info(f"✅ Actividad encontrada: {actividad}")
                
                cuota = CuotaEstudiante.objects.get(estudiante=estudiante, actividad=actividad)
                logger.info(f"✅ Cuota encontrada: {cuota} - Estado: {cuota.estado}")
                
            except Estudiante.DoesNotExist:
                logger.error(f"❌ Estudiante con ID {estudiante_id} no encontrado")
                messages.error(request, f'Estudiante con ID {estudiante_id} no encontrado.')
                return redirect('cuotas:registrar_pago')
            except Actividad.DoesNotExist:
                logger.error(f"❌ Actividad '{actividad_nombre}' no encontrada")
                messages.error(request, f'Actividad "{actividad_nombre}" no encontrada.')
                return redirect('cuotas:registrar_pago')
            except CuotaEstudiante.DoesNotExist:
                logger.error(f"❌ No se encontró cuota para {estudiante_id} y actividad '{actividad_nombre}'")
                messages.error(request, f'No se encontró una cuota para {estudiante} y la actividad "{actividad_nombre}".')
                return redirect('cuotas:registrar_pago')
            except Exception as e:
                logger.error(f"💥 Error inesperado al buscar datos: {e}", exc_info=True)
                messages.error(request, f'Error inesperado: {e}')
                return redirect('cuotas:registrar_pago')
                
            # Registrar el pago
            try:
                logger.info(f"💳 Creando pago - Cuota: {cuota.id}, Monto: {monto}")
                pago = PagoCuota.objects.create(
                    cuota=cuota,
                    monto=monto,
                    metodo_pago=metodo,
                    observacion=observacion,
                )
                logger.info(f"✅ Pago creado: {pago.id}")
                
                # Actualizar monto pagado y estado de la cuota
                monto_anterior = cuota.monto_pagado
                cuota.monto_pagado += monto
                logger.info(f"💰 Actualizando cuota - Anterior: {monto_anterior}, Nuevo: {cuota.monto_pagado}, Total: {cuota.monto_total}")
                
                if cuota.monto_pagado >= cuota.monto_total:
                    cuota.estado = 'pagado'
                    tipo_notificacion = 'pago_confirmado'
                    mensaje_notif = f'El pago de ${monto:,.0f} para {cuota.actividad.nombre} ha sido registrado exitosamente. La cuota está completamente pagada.'
                    logger.info("✅ Cuota completamente pagada")
                else:
                    cuota.estado = 'pendiente'
                    tipo_notificacion = 'pago_parcial'
                    saldo_restante = cuota.monto_total - cuota.monto_pagado
                    mensaje_notif = f'Se ha registrado un pago parcial de ${monto:,.0f} para {cuota.actividad.nombre}. Saldo pendiente: ${saldo_restante:,.0f}.'
                    logger.info(f"⚠️ Pago parcial - Saldo restante: {saldo_restante}")
                
                cuota.save()
                logger.info("✅ Cuota actualizada y guardada")
                
                # Crear notificación automática PARA EL APODERADO
                try:
                    from core.models import Notificacion
                    from django.contrib.auth.models import User
                    
                    apoderado = estudiante.apoderado
                    logger.info(f"👤 Creando notificación para apoderado: {apoderado.nombre} {apoderado.apellido_paterno}")
                    
                    # Obtener usuario admin o crear uno si no existe
                    if request.user.is_authenticated:
                        usuario_registra = request.user
                    else:
                        usuario_registra, created = User.objects.get_or_create(
                            username='sistema',
                            defaults={'first_name': 'Sistema', 'last_name': 'Automatico'}
                        )
                    
                    notificacion = Notificacion.objects.create(
                    usuario_registra=usuario_registra,
                    apoderado_nombre=f'{apoderado.nombre} {apoderado.apellido_paterno} {apoderado.apellido_materno}',
                    apoderado_email=apoderado.email,
                    apoderado_telefono=apoderado.telefono,
                    apoderado_rut=apoderado.rut,
                    titulo=f'Notificación de Pago - {estudiante.nombre} {estudiante.apellido_paterno}',
                    mensaje=f'Estimado/a {apoderado.nombre} {apoderado.apellido_paterno}, {mensaje_notif} El pago fue realizado mediante {metodo}. Fecha: {timezone.now().strftime("%d/%m/%Y %H:%M")}',
                    tipo=tipo_notificacion,
                    estudiante=estudiante,  # ✅ Aquí se vincula correctamente
                    actividad_nombre=cuota.actividad.nombre,
                    monto=monto,
                    metodo_pago=metodo,
                    estado='enviada'
                    )
                    logger.info(f"✅ Notificación creada: {notificacion.id}")
                    
                    messages.success(request, f'Pago de ${monto:,.0f} registrado exitosamente. Se ha enviado notificación automática.')
                    logger.info("🎉 Proceso completado exitosamente")
                    return redirect('cuotas:registrar_pago')
                    
                except Exception as e:
                    logger.error(f"❌ Error al crear notificación: {e}", exc_info=True)
                    messages.warning(request, f'Pago registrado exitosamente, pero hubo un error al enviar la notificación: {e}')
                    return redirect('cuotas:registrar_pago')
                
            except Exception as e:
                logger.error(f"💥 Error general al registrar el pago: {e}", exc_info=True)
                messages.error(request, f'Error al registrar el pago: {e}')
                return redirect('cuotas:registrar_pago')
    else:
        logger.info("📄 Cargando formulario GET - Registrar Pago")
        form = PagoCuotaForm()
    
    # Cargar datos reales desde la base de datos
    from estudiantes.models import Estudiante
    from actividades.models import Actividad
    from .models import CuotaEstudiante
    
    logger.debug("🔍 Buscando cuotas pendientes...")
    
    # Obtener solo estudiantes con cuotas pendientes
    cuotas_pendientes = CuotaEstudiante.objects.select_related('estudiante', 'actividad').filter(estado='pendiente')
    
    logger.info(f"📊 Total cuotas pendientes encontradas: {len(cuotas_pendientes)}")
    
    estudiantes_con_deuda = []
    actividades_set = set()
    
    for cuota in cuotas_pendientes:
        saldo_pendiente = cuota.saldo_pendiente()
        logger.debug(f"💰 {cuota.estudiante.nombre}: Saldo pendiente = ${saldo_pendiente}")
        if saldo_pendiente > 0:  # Solo mostrar si realmente hay saldo pendiente
            estudiantes_con_deuda.append({
                'id': cuota.estudiante.id,
                'nombre': f"{cuota.estudiante.nombre} {cuota.estudiante.apellido_paterno} {cuota.estudiante.apellido_materno}",
                'rut': cuota.estudiante.rut,
                'actividad': cuota.actividad.nombre,
                'saldo_pendiente': saldo_pendiente
            })
            actividades_set.add((cuota.actividad.nombre, cuota.monto_total))
    
    logger.info(f"✅ Estudiantes con deuda encontrados: {len(estudiantes_con_deuda)}")
    logger.info(f"📚 Actividades disponibles: {len(actividades_set)}")
    
    # Remover duplicados y ordenar estudiantes
    estudiantes_con_deuda = sorted(estudiantes_con_deuda, key=lambda x: x['nombre'])
    
    # Crear lista de actividades disponibles
    actividades_disponibles = [
        {'nombre': nombre, 'valor': int(valor)} 
        for nombre, valor in sorted(actividades_set)
    ]

    # Generar saldos por estudiante y actividad - SOLO para combinaciones válidas
    saldos = {}
    for estudiante in estudiantes_con_deuda:
        if estudiante['id'] not in saldos:
            saldos[estudiante['id']] = {}
        # Solo agregar las actividades para las que este estudiante tiene cuotas pendientes
        cuota = cuotas_pendientes.filter(
            estudiante_id=estudiante['id'], 
            actividad__nombre=estudiante['actividad']
        ).first()
        if cuota:
            saldos[estudiante['id']][estudiante['actividad']] = cuota.saldo_pendiente()
    
    # También necesitamos agregar ceros para actividades que no tienen
    for estudiante in estudiantes_con_deuda:
        for actividad in actividades_disponibles:
            if actividad['nombre'] not in saldos[estudiante['id']]:
                saldos[estudiante['id']][actividad['nombre']] = 0

    context = {
        'form': form,
        'estudiantes_con_deuda': estudiantes_con_deuda,
        'actividades_disponibles': actividades_disponibles,
        'saldos': saldos
    }

    return render(request, 'cuotas/registrar_pago.html', context)

def historial_actividad(request, actividad_id):
    """RF-09: Consultar el historial de cuotas vinculadas a actividad específica"""
    
    # Simular datos del historial de una actividad específica
    actividades_disponibles = {
        1: {
            'nombre': 'Gira de Estudios 8° Básico',
            'tipo': 'Gira Educativa',
            'monto_por_estudiante': 25000,
            'fecha_inicio': '2024-03-15',
            'fecha_fin': '2024-03-17',
            'cursos': '8° Básico A, 8° Básico B'
        },
        2: {
            'nombre': 'Uniforme Deportivo',
            'tipo': 'Material Escolar',
            'monto_por_estudiante': 15000,
            'fecha_inicio': '2024-02-01',
            'fecha_fin': '2024-02-28',
            'cursos': 'Todos los cursos'
        },
        3: {
            'nombre': 'Seguro Escolar Anual',
            'tipo': 'Seguro',
            'monto_por_estudiante': 12000,
            'fecha_inicio': '2024-03-01',
            'fecha_fin': '2024-12-31',
            'cursos': 'Todos los cursos'
        }
    }
    
    actividad = actividades_disponibles.get(actividad_id, actividades_disponibles[1])
    
    # Simular historial de pagos para esta actividad
    historial_pagos = [
        {
            'estudiante': 'María González Pérez',
            'rut': '20.123.456-7',
            'curso': '8° Básico A',
            'monto_total': actividad['monto_por_estudiante'],
            'monto_pagado': actividad['monto_por_estudiante'],
            'fecha_pago': '2024-03-08',
            'metodo_pago': 'Transferencia',
            'estado': 'Pagado',
            'comprobante': 'TRF-001234'
        },
        {
            'estudiante': 'Carlos Mendoza Torres',
            'rut': '20.789.012-3',
            'curso': '8° Básico A',
            'monto_total': actividad['monto_por_estudiante'],
            'monto_pagado': actividad['monto_por_estudiante'],
            'fecha_pago': '2024-03-10',
            'metodo_pago': 'Efectivo',
            'estado': 'Pagado',
            'comprobante': 'EFE-005678'
        },
        {
            'estudiante': 'Valentina Ruiz Soto',
            'rut': '20.345.678-9',
            'curso': '8° Básico B',
            'monto_total': actividad['monto_por_estudiante'],
            'monto_pagado': actividad['monto_por_estudiante'] // 2,
            'fecha_pago': '2024-03-05',
            'metodo_pago': 'Transferencia',
            'estado': 'Parcial',
            'comprobante': 'TRF-002345'
        },
        {
            'estudiante': 'Sebastián López Vera',
            'rut': '20.456.789-0',
            'curso': '8° Básico B',
            'monto_total': actividad['monto_por_estudiante'],
            'monto_pagado': 0,
            'fecha_pago': None,
            'metodo_pago': None,
            'estado': 'Pendiente',
            'comprobante': None
        }
    ]
    
    # Calcular estadísticas
    total_estudiantes = len(historial_pagos)
    pagos_completos = len([p for p in historial_pagos if p['estado'] == 'Pagado'])
    pagos_parciales = len([p for p in historial_pagos if p['estado'] == 'Parcial'])
    pagos_pendientes = len([p for p in historial_pagos if p['estado'] == 'Pendiente'])
    
    recaudacion_total = sum([p['monto_pagado'] for p in historial_pagos])
    recaudacion_esperada = total_estudiantes * actividad['monto_por_estudiante']
    
    context = {
        'actividad': actividad,
        'actividad_id': actividad_id,
        'historial_pagos': historial_pagos,
        'estadisticas': {
            'total_estudiantes': total_estudiantes,
            'pagos_completos': pagos_completos,
            'pagos_parciales': pagos_parciales,
            'pagos_pendientes': pagos_pendientes,
            'recaudacion_total': recaudacion_total,
            'recaudacion_esperada': recaudacion_esperada,
            'porcentaje_recaudacion': (recaudacion_total / recaudacion_esperada * 100) if recaudacion_esperada > 0 else 0
        }
    }
    
    return render(request, 'cuotas/historial_actividad.html', context)

def exportar_pagos(request):
    """RF-05: Exportar información en PDF y Excel"""
    formato = request.GET.get('formato', 'excel')
    
    if formato == 'pdf':
        # Simular exportación PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pagos_estudiantes.pdf"'
        response.write(b'%PDF-1.4\n%Simulated PDF content for payments export')
        return response
    
    elif formato == 'excel':
        # Simular exportación Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="pagos_estudiantes.xlsx"'
        response.write(b'Simulated Excel content for payments export')
        return response
    
    else:
        messages.error(request, 'Formato de exportación no válido.')
        return redirect('cuotas:lista_pagos')

def estado_pago_apoderado(request):
    """RF-02: Visualizar el estado de pago por apoderado"""
    
    # Simular datos del apoderado actual
    apoderado_actual = {
        'nombre': 'Juan Pérez González',
        'rut': '12.345.678-9',
        'estudiantes': [
            {
                'nombre': 'María Pérez Soto',
                'rut': '20.123.456-7',
                'curso': '8° Básico A',
                'cuotas': [
                    {
                        'actividad': 'Gira de Estudios 8° Básico',
                        'monto_total': 25000,
                        'monto_pagado': 25000,
                        'saldo_pendiente': 0,
                        'estado': 'Pagado',
                        'fecha_vencimiento': '2024-03-10',
                        'fecha_pago': '2024-03-08'
                    },
                    {
                        'actividad': 'Ceremonia de Graduación',
                        'monto_total': 35000,
                        'monto_pagado': 0,
                        'saldo_pendiente': 35000,
                        'estado': 'Pendiente',
                        'fecha_vencimiento': '2024-12-10',
                        'fecha_pago': None
                    }
                ]
            },
            {
                'nombre': 'Carlos Pérez Soto',
                'rut': '20.234.567-8',
                'curso': '6° Básico A',
                'cuotas': [
                    {
                        'actividad': 'Material Escolar 2024',
                        'monto_total': 8500,
                        'monto_pagado': 8500,
                        'saldo_pendiente': 0,
                        'estado': 'Pagado',
                        'fecha_vencimiento': '2024-01-30',
                        'fecha_pago': '2024-01-25'
                    },
                    {
                        'actividad': 'Seguro Escolar Anual',
                        'monto_total': 12000,
                        'monto_pagado': 6000,
                        'saldo_pendiente': 6000,
                        'estado': 'Parcial',
                        'fecha_vencimiento': '2024-03-15',
                        'fecha_pago': '2024-03-01'
                    }
                ]
            }
        ]
    }
    
    # Calcular totales
    total_pendiente = 0
    total_pagado = 0
    
    for estudiante in apoderado_actual['estudiantes']:
        for cuota in estudiante['cuotas']:
            total_pendiente += cuota['saldo_pendiente']
            total_pagado += cuota['monto_pagado']
    
    context = {
        'apoderado': apoderado_actual,
        'total_pendiente': total_pendiente,
        'total_pagado': total_pagado,
        'total_general': total_pendiente + total_pagado
    }
    
    return render(request, 'cuotas/estado_apoderado.html', context)
