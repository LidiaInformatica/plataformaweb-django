__pycache__  test_model_perfilusuario.py
root@70271cb92218:/app# touch tests/core/__init__.py
root@70271cb92218:/app# ls tests/core
__init__.py  __pycache__  test_model_perfilusuario.py
root@70271cb92218:/app# PYTHONPATH=. pytest tests/core/test_model_perfilusuario.py -v
================================================================ test session starts ================================================================platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 4.2.7, settings: plataformaweb.settings (from ini)
rootdir: /app
configfile: pytest.ini
plugins: django-4.11.1
collected 1 item

tests/core/test_model_perfilusuario.py::test_user_str FAILED                                                                                  [100%]

===================================================================== FAILURES ======================================================================___________________________________________________________________ test_user_str ___________________________________________________________________
    @pytest.mark.django_db
    def test_user_str():
        User = get_user_model()
        user = User.objects.create_user(username="lidia", password="admin123")
>       perfil = PerfilUsuario.objects.create(usuario=user, nombre="Presidente", tipo="admin")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/core/test_model_perfilusuario.py:9:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:656: in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
self = <PerfilUsuario:  - Sin tipo>, args = (), kwargs = {'nombre': 'Presidente', 'tipo': 'admin'}, cls = <class 'core.models.PerfilUsuario'>        
opts = <Options for PerfilUsuario>, _setattr = <built-in function setattr>, _DEFERRED = <Deferred field>
fields_iter = <tuple_iterator object at 0x709800bf0ac0>, val = None, field = <django.db.models.fields.DateTimeField: fecha_creacion>
is_related_object = False, rel_obj = <User: lidia>, property_names = frozenset({'pk'})

    def __init__(self, *args, **kwargs):
        # Alias some things as locals to avoid repeat global lookups
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED
        if opts.abstract:
            raise TypeError("Abstract models cannot be instantiated.")

        pre_init.send(sender=cls, args=args, kwargs=kwargs)

        # Set up the storage for instance state
        self._state = ModelState()

        # There is a rather weird disparity here; if kwargs, it's set, then args
        # overrides it. It should be one or the other; don't duplicate the work
        # The reason for the kwargs check is that standard iterator passes in by
        # args, and instantiation for iteration is 33% faster.
        if len(args) > len(opts.concrete_fields):
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")

        if not kwargs:
            fields_iter = iter(opts.concrete_fields)
            # The ordering of the zip calls matter - zip throws StopIteration
            # when an iter throws it. So if the first iter throws it, the second
            # is *not* consumed. We rely on this, so don't change the order
            # without changing the logic.
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
        else:
            # Slower, kwargs-ready version.
            fields_iter = iter(opts.fields)
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
                if kwargs.pop(field.name, NOT_PROVIDED) is not NOT_PROVIDED:
                    raise TypeError(
                        f"{cls.__qualname__}() got both positional and "
                        f"keyword arguments for field '{field.name}'."
                    )

        # Now we're left with the unprocessed fields that *must* come from
        # keywords, or default.

        for field in fields_iter:
            is_related_object = False
            # Virtual field
            if field.attname not in kwargs and field.column is None:
                continue
            if kwargs:
                if isinstance(field.remote_field, ForeignObjectRel):
                    try:
                        # Assume object instance was passed in.
                        rel_obj = kwargs.pop(field.name)
                        is_related_object = True
                    except KeyError:
                        try:
                            # Object instance wasn't passed in -- must be an ID.
                            val = kwargs.pop(field.attname)
                        except KeyError:
                            val = field.get_default()
                else:
                    try:
                        val = kwargs.pop(field.attname)
                    except KeyError:
                        # This is done with an exception rather than the
                        # default argument on pop because we don't want
                        # get_default() to be evaluated, and then not used.
                        # Refs #12057.
                        val = field.get_default()
            else:
                val = field.get_default()

            if is_related_object:
                # If we are passed a related instance, set it using the
                # field.name instead of field.attname (e.g. "user" instead of
                # "user_id") so that the object gets properly cached (and type
                # checked) by the RelatedObjectDescriptor.
                if rel_obj is not _DEFERRED:
                    _setattr(self, field.name, rel_obj)
            else:
                if val is not _DEFERRED:
                    _setattr(self, field.attname, val)

        if kwargs:
            property_names = opts._property_names
            unexpected = ()
            for prop, value in kwargs.items():
                # Any remaining kwargs must correspond to properties or virtual
                # fields.
                if prop in property_names:
                    if value is not _DEFERRED:
                        _setattr(self, prop, value)
                else:
                    try:
                        opts.get_field(prop)
                    except FieldDoesNotExist:
                        unexpected += (prop,)
                    else:
                        if value is not _DEFERRED:
                            _setattr(self, prop, value)
            if unexpected:
                unexpected_names = ", ".join(repr(n) for n in unexpected)
>               raise TypeError(
                    f"{cls.__name__}() got unexpected keyword arguments: "
                    f"{unexpected_names}"
                )
E               TypeError: PerfilUsuario() got unexpected keyword arguments: 'nombre', 'tipo'

/usr/local/lib/python3.12/site-packages/django/db/models/base.py:567: TypeError
--------------------------------------------------------------- Captured stderr setup ---------------------------------------------------------------Creating test database for alias 'default'...
------------------------------------------------------------- Captured stderr teardown --------------------------------------------------------------Destroying test database for alias 'default'...
============================================================== short test summary info ==============================================================FAILED tests/core/test_model_perfilusuario.py::test_user_str - TypeError: PerfilUsuario() got unexpected keyword arguments: 'nombre', 'tipo'
================================================================= 1 failed in 1.24s =================================================================root@70271cb92218:/app#
