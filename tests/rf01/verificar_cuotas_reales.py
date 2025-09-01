import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plataformaweb.settings")
django.setup()

from cuotas.models import CuotaEstudiante

cuotas_validas = CuotaEstudiante.objects.filter(actividad__isnull=False).distinct()
total = cuotas_validas.count()

print(f"[VALIDACIÓN FUNCIONAL REAL] Cuotas vinculadas a actividades: {total}")
