import os
import re
from pathlib import Path

def analyze_templates():
    """Analiza qué templates están siendo utilizados"""
    
    # 1. Encontrar todos los templates
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print("📁 TEMPLATES ENCONTRADOS:")
    for template in sorted(html_files):
        print(f"  - {template}")
    
    # 2. Encontrar referencias en views.py
    view_references = set()
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'views.py':
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Buscar render() calls
                        renders = re.findall(r'render\([^,]+,\s*[\'"]([^\'\"]+)[\'"]', content)
                        view_references.update(renders)
                        if renders:
                            print(f"\n📋 REFERENCIAS EN {filepath}:")
                            for ref in renders:
                                print(f"  - {ref}")
                except Exception as e:
                    print(f"Error leyendo {filepath}: {e}")
    
    # 3. Encontrar referencias en urls.py
    url_references = set()
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'urls.py':
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Buscar template references
                        templates = re.findall(r'[\'"]([^\'\"]+\.html)[\'"]', content)
                        url_references.update(templates)
                        if templates:
                            print(f"\n🔗 REFERENCIAS EN {filepath}:")
                            for ref in templates:
                                print(f"  - {ref}")
                except Exception as e:
                    print(f"Error leyendo {filepath}: {e}")
    
    # 4. Encontrar extends e includes
    template_dependencies = set()
    for template in html_files:
        try:
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
                # Buscar extends
                extends = re.findall(r'{%\s*extends\s*[\'"]([^\'\"]+)[\'"]', content)
                template_dependencies.update(extends)
                # Buscar includes
                includes = re.findall(r'{%\s*include\s*[\'"]([^\'\"]+)[\'"]', content)
                template_dependencies.update(includes)
        except Exception as e:
            print(f"Error leyendo {template}: {e}")
    
    print("\n🔗 DEPENDENCIAS ENTRE TEMPLATES:")
    for dep in sorted(template_dependencies):
        print(f"  - {dep}")
    
    # 5. Identificar templates no utilizados
    all_references = view_references | url_references | template_dependencies
    
    unused_templates = []
    for template in html_files:
        template_name = os.path.basename(template)
        # También verificar path relativo común
        relative_path = template.replace('\\', '/').replace('./templates/', '')
        
        is_used = False
        for ref in all_references:
            if (template_name in ref or 
                relative_path in ref or 
                template.endswith(ref) or
                ref in template or
                template_name == ref):
                is_used = True
                break
        
        if not is_used:
            unused_templates.append(template)
    
    print("\n🗑️ TEMPLATES APARENTEMENTE NO UTILIZADOS:")
    if unused_templates:
        for template in unused_templates:
            print(f"  ❌ {template}")
    else:
        print("  ✅ Todos los templates están siendo utilizados")
    
    print(f"\n📊 RESUMEN:")
    print(f"  - Total templates: {len(html_files)}")
    print(f"  - Referencias encontradas: {len(all_references)}")
    print(f"  - Templates no utilizados: {len(unused_templates)}")
    
    return unused_templates, all_references

if __name__ == "__main__":
    print("🧹 ANALIZADOR DE TEMPLATES NO UTILIZADOS")
    print("=" * 50)
    
    unused, references = analyze_templates()
    
    if unused:
        print("\n⚠️  ¿DESEAS ELIMINAR ESTOS ARCHIVOS? (s/n)")
        respuesta = input().lower()
        if respuesta == 's':
            print("\n🗑️ ELIMINANDO ARCHIVOS...")
            for template in unused:
                try:
                    os.remove(template)
                    print(f"✅ Eliminado: {template}")
                except Exception as e:
                    print(f"❌ Error eliminando {template}: {e}")
        else:
            print("🚫 Operación cancelada")
    else:
        print("\n🎉 ¡No hay templates para limpiar!")