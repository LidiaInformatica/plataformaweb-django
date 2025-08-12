from django.core.management.base import BaseCommand
from estudiantes.models import Curso, Apoderado, Estudiante
from actividades.models import TipoActividad, Actividad
from cuotas.models import CuotaEstudiante
from datetime import date

class Command(BaseCommand):
    help = 'Carga datos iniciales de estudiantes, actividades, cursos y cuotas simuladas'

    def handle(self, *args, **options):
        # Crear cursos
        cursos_data = [
            {'nombre': 'Pre Kinder', 'nivel': 'Preescolar', 'año': 2025},
            {'nombre': 'Kinder', 'nivel': 'Preescolar', 'año': 2025},
            {'nombre': '1° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '2° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '3° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '4° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '5° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '6° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '7° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '8° Básico', 'nivel': 'Básico', 'año': 2025},
            {'nombre': '1° Medio', 'nivel': 'Medio', 'año': 2025},
            {'nombre': '2° Medio', 'nivel': 'Medio', 'año': 2025},
            {'nombre': '3° Medio', 'nivel': 'Medio', 'año': 2025},
            {'nombre': '4° Medio', 'nivel': 'Medio', 'año': 2025},
        ]
        cursos = {}
        for c in cursos_data:
            obj, _ = Curso.objects.get_or_create(nombre=c['nombre'], nivel=c['nivel'], año=c['año'])
            cursos[c['nombre']] = obj

        # Crear apoderado único para todos
        apoderado, _ = Apoderado.objects.get_or_create(
            rut='12.345.678-9', nombre='Juan', apellido_paterno='Pérez', apellido_materno='González',
            telefono='912345678', email='juan.perez@email.com'
        )

        # Crear estudiantes
        estudiantes_data = [
            {'rut': '20.123.456-7', 'nombre': 'María', 'apellido_paterno': 'González', 'apellido_materno': 'Pérez', 'curso': '8° Básico'},
            {'rut': '20.234.567-8', 'nombre': 'Carlos', 'apellido_paterno': 'Rodríguez', 'apellido_materno': 'Silva', 'curso': '7° Básico'},
            {'rut': '20.345.678-9', 'nombre': 'Ana', 'apellido_paterno': 'Martínez', 'apellido_materno': 'López', 'curso': '6° Básico'},
            {'rut': '20.456.789-0', 'nombre': 'Diego', 'apellido_paterno': 'Fernández', 'apellido_materno': 'Castro', 'curso': '5° Básico'},
            {'rut': '20.567.890-1', 'nombre': 'Sofía', 'apellido_paterno': 'Herrera', 'apellido_materno': 'Morales', 'curso': '4° Básico'},
            {'rut': '20.678.901-2', 'nombre': 'Martín', 'apellido_paterno': 'Silva', 'apellido_materno': 'Rojas', 'curso': '8° Básico'},
            # ...agrega los otros estudiantes aquí...
        ]
        estudiantes = {}
        for e in estudiantes_data:
            obj, _ = Estudiante.objects.get_or_create(
                rut=e['rut'], nombre=e['nombre'], apellido_paterno=e['apellido_paterno'], apellido_materno=e['apellido_materno'],
                fecha_nacimiento=date(2010, 1, 1), curso=cursos[e['curso']], apoderado=apoderado, vinculo_apoderado='padre'
            )
            estudiantes[e['rut']] = obj

        # Crear tipos de actividad
        tipo, _ = TipoActividad.objects.get_or_create(nombre='General', descripcion='Actividades escolares')

        # Crear actividades
        actividades_data = [
            {'nombre': 'Gira de Estudios 8° Básico', 'monto': 25000, 'cursos': ['8° Básico']},
            {'nombre': 'Uniforme Deportivo', 'monto': 15000, 'cursos': ['7° Básico', '8° Básico']},
            {'nombre': 'Seguro Escolar Anual', 'monto': 12000, 'cursos': ['Todos los cursos']},
            {'nombre': 'Material Escolar 2025', 'monto': 8500, 'cursos': ['6° Básico']},
            {'nombre': 'Actividades Extraprogramáticas', 'monto': 18000, 'cursos': ['4° Básico']},
            {'nombre': 'Ceremonia de Graduación', 'monto': 35000, 'cursos': ['8° Básico']},
            {'nombre': 'Gala de 4° Medio', 'monto': 20000, 'cursos': ['4° Medio']},
            {'nombre': 'Gala de 8° Básico', 'monto': 30000, 'cursos': ['8° Básico']},
            # ...agrega las demás actividades aquí...
        ]
        actividades = {}
        for a in actividades_data:
            obj, _ = Actividad.objects.get_or_create(
                nombre=a['nombre'], tipo=tipo, descripcion=a['nombre'], fecha_inicio=date(2025, 3, 1), fecha_fin=date(2025, 12, 31), monto_por_estudiante=a['monto']
            )
            for curso_nombre in a['cursos']:
                if curso_nombre == 'Todos los cursos':
                    obj.cursos_asignados.set(Curso.objects.all())
                else:
                    obj.cursos_asignados.add(cursos[curso_nombre])
            actividades[a['nombre']] = obj

        # Crear cuotas simuladas
        cuotas_data = [
            {'rut': '20.123.456-7', 'actividad': 'Gira de Estudios 8° Básico', 'monto_total': 25000, 'monto_pagado': 25000, 'estado': 'pagado', 'fecha_vencimiento': date(2025, 3, 10)},
            {'rut': '20.234.567-8', 'actividad': 'Uniforme Deportivo', 'monto_total': 15000, 'monto_pagado': 15000, 'estado': 'pagado', 'fecha_vencimiento': date(2025, 2, 25)},
            {'rut': '20.345.678-9', 'actividad': 'Material Escolar 2025', 'monto_total': 8500, 'monto_pagado': 8500, 'estado': 'pagado', 'fecha_vencimiento': date(2025, 1, 30)},
            {'rut': '20.456.789-0', 'actividad': 'Seguro Escolar Anual', 'monto_total': 12000, 'monto_pagado': 6000, 'estado': 'pendiente', 'fecha_vencimiento': date(2025, 3, 15)},
            {'rut': '20.567.890-1', 'actividad': 'Actividades Extraprogramáticas', 'monto_total': 18000, 'monto_pagado': 0, 'estado': 'pendiente', 'fecha_vencimiento': date(2025, 4, 5)},
            {'rut': '20.678.901-2', 'actividad': 'Ceremonia de Graduación', 'monto_total': 35000, 'monto_pagado': 0, 'estado': 'pendiente', 'fecha_vencimiento': date(2025, 12, 10)},
            # ...agrega las demás cuotas aquí...
        ]
        for c in cuotas_data:
            CuotaEstudiante.objects.get_or_create(
                estudiante=estudiantes[c['rut']], actividad=actividades[c['actividad']],
                monto_total=c['monto_total'], monto_pagado=c['monto_pagado'], estado=c['estado'], fecha_vencimiento=c['fecha_vencimiento']
            )

        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente.'))
