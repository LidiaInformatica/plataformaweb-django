import os
import re

#  Carpetas activas (ajustá según tu estructura)
TEMPLATE_DIRS = [
    "templates",
    "templates/notificaciones",
    "templates/dashboard",
    "templates/mensajes"
]

#  Carpetas excluidas (no deberían contener templates activos)
EXCLUDED_DIRS = [
    "templates_backup",
    "scripts_backup",
    "static",
    "styles"
]

#  Archivos donde buscar renderizaciones
VIEWS_DIR = "."

#  Regex para detectar render(request, 'template.html')
RENDER_REGEX = re.compile(r"render\s*\(\s*request\s*,\s*['\"]([^'\"]+)['\"]")

#  Resultados
referenced_templates = set()
found_templates = set()
excluded_templates = set()
missing_templates = set()

#  Buscar templates referenciados
for root, _, files in os.walk(VIEWS_DIR):
    for file in files:
        if file.endswith(".py") and "notificacion" in file.lower():
            with open(os.path.join(root, file), encoding="utf-8") as f:
                content = f.read()
                matches = RENDER_REGEX.findall(content)
                referenced_templates.update(matches)

#  Buscar templates existentes
for template in referenced_templates:
    found = False
    for dir in TEMPLATE_DIRS:
        path = os.path.join(dir, template)
        if os.path.exists(path):
            found_templates.add(template)
            found = True
            break
    if not found:
        for dir in EXCLUDED_DIRS:
            path = os.path.join(dir, template)
            if os.path.exists(path):
                excluded_templates.add(template)
                found = True
                break
    if not found:
        missing_templates.add(template)

#  Reporte
print("\n Auditoría de templates para notificaciones")
print(" Encontrados en carpetas activas:")
for t in sorted(found_templates):
    print(f"  - {t}")

print("\n Encontrados en carpetas excluidas:")
for t in sorted(excluded_templates):
    print(f"  - {t}")

print("\n No encontrados:")
for t in sorted(missing_templates):
    print(f"  - {t}")