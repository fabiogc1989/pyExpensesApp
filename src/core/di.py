import functools
import inspect
from typing import Annotated, Type, get_args, get_origin


class Dependency:
    def __init__(self, name: str):
        self.name = name


class DependencyError(Exception):
    """Custom exception for DI failures."""

    pass


class LazyProxy:
    """A proxy that delays the instantiation of the actual object until it's needed."""

    def __init__(self, container, cls, name):
        self._container = container
        self._cls = cls
        self._name = name
        self._instance = None

    def _get_real_instance(self):
        if self._instance is None:
            self._instance = self._container._resolve(self._cls, self._name)
        return self._instance

    def __getattr__(self, name):
        return getattr(self._get_real_instance(), name)


class Inject:
    def __init__(self, cls: Type, name: str = 'default'):
        self.target_cls = cls
        self.target_name = name
        self.attr_name: str = ''  # Será preenchido pelo Python em __set_name__

    def __set_name__(self, owner, name):
        # O Python chama isso automaticamente para saber o nome da variável
        self.attr_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Resolve a instância real através do container global (ou proxy)
        # Aqui usamos o LazyProxy para manter a consistência do seu código original
        proxy = LazyProxy(ioc, self.target_cls, self.target_name)

        # Opcional: Cache do proxy na instância para evitar recriação do objeto Proxy
        value = proxy._get_real_instance()
        setattr(instance, self.attr_name, value)
        return value


class Container:
    def __init__(self):
        self._registry = {}  # Stores the class/factory
        self._instances = {}  # Cache for singletons

    def register(self, cls, name='default'):
        """Just record the class; don't instantiate yet."""
        self._registry[(cls, name)] = cls
        return cls

    def _resolve(self, cls: Type, name: str):
        """Internal resolver that manages the object lifecycle."""
        if (cls, name) not in self._registry:
            raise DependencyError(
                f'Service {cls.__name__} (name: {name}) not registered!'
            )

        # Instantiate if not already cached
        if (cls, name) not in self._instances:
            # We create the instance only when the Proxy asks for it
            self._instances[(cls, name)] = self._registry[(cls, name)]()
        return self._instances[(cls, name)]


# Initialize our global container
ioc = Container()
