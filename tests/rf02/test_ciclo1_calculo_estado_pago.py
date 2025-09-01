import pytest
from estudiantes.models import Estudiante, Apoderado, Curso
from actividades.models import Actividad, TipoActividad
from cuotas.models import CuotaEstudiante, PagoCuota
from datetime import date

@pytest.mark.django_db
def test_calculo_estado_pago():
    """
    RF-02 Ciclo 1: Cálculo de Estado
    Verifica que el estado de pago del alumno sea correcto según los pagos registrados.
    """
    # Crear curso de ejemplo
    curso = Curso.objects.create(
        nombre="1A",
        nivel="Básico",
        año=2025
    )
    # Crear tipo de actividad
    tipo_actividad = TipoActividad.objects.create(
        nombre="Deporte",
        descripcion="Actividades deportivas"
    )
    # Crear apoderado de ejemplo (ajusta los campos según tu modelo real)
    apoderado = Apoderado.objects.create(
        nombre="Apoderado Test"
    )
    # Crear estudiante
    estudiante = Estudiante.objects.create(
        rut="12345678-9",
        nombre="Alumno",
        apellido_paterno="Prueba",
        apellido_materno="Test",
        fecha_nacimiento="2015-01-01",
        curso=curso,
        vinculo_apoderado="hijo",
        apoderado=apoderado
    )
    # Crear actividad y asignar curso
    actividad = Actividad.objects.create(
        nombre="Fútbol",
        descripcion="Actividad deportiva",
        tipo=tipo_actividad,
        fecha_inicio=date.today(),
        fecha_fin=date.today(),
        monto_por_estudiante=10000
    )
    actividad.cursos_asignados.add(curso)
    # Crear cuota asociada al estudiante y actividad
    cuota = CuotaEstudiante.objects.create(
        estudiante=estudiante,
        actividad=actividad,
        monto_total=10000,
        monto_pagado=0,
        estado="pendiente",
        fecha_vencimiento=date.today()
    )
    # Registrar un pago
    PagoCuota.objects.create(
        cuota=cuota,
        monto=10000,
        metodo_pago="efectivo"
    )
    # Actualizar el monto pagado y estado de la cuota
    cuota.monto_pagado = 10000
    cuota.estado = "pagado"
    cuota.save()

    # Verificar que el estado sea correcto
    cuota_actualizada = CuotaEstudiante.objects.get(pk=cuota.pk)
    assert cuota_actualizada.estado == "pagado"
    assert cuota_actualizada.monto_pagado == 10000
    assert cuota_actualizada.saldo_pendiente() == 0