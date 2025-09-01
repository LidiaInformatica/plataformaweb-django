from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def grupo_requerido(grupo_nombre):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.groups.filter(name=grupo_nombre).exists():
                if grupo_nombre == 'Apoderado':
                    return redirect('dashboard_directiva')
                return redirect('dashboard_apoderado')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator