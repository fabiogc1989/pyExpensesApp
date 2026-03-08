import functools
import inspect
from typing import Annotated, Type, get_origin, get_args


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


class Container:
    def __init__(self):
        self._registry = {} # Stores the class/factory
        self._instances = {} # Cache for singletons
    
    def register(self, cls, name = 'default'):
        """Just record the class; don't instantiate yet."""
        self._registry[(cls, name)] = cls
        return cls
    
    def _resolve(self, cls: Type, name: str):
        """Internal resolver that manages the object lifecycle."""
        if (cls, name) not in self._registry:
            raise DependencyError(f"Service {cls.__name__} (name: {name}) not registered!")
        
        # Instantiate if not already cached
        if (cls, name) not in self._instances:
            # We create the instance only when the Proxy asks for it
            self._instances[(cls, name)] = self._registry[(cls, name)]()
        return self._instances[(cls, name)]

    def inject(self,func):
            """Decorator to inject dependencies via type hints."""
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                bound_args = sig.bind_partial(*args, **kwargs)

                for name, param in sig.parameters.items():
                    if name in bound_args.arguments: continue # Skip if already provided

                    # Extract type and name from Annotated
                    annotation = param.annotation
                    target_cls, target_name = annotation, 'default'

                    if get_origin(annotation) is Annotated:
                       args_cls = get_args(annotation)
                       target_cls = args_cls[0]
                       meta = args_cls[1]
                       if isinstance(meta, Dependency):
                           target_name = meta.name
                        
                    if (target_cls, target_name) in self._registry:
                        kwargs[name] = LazyProxy(self, target_cls, target_name)

                return func(*args, **kwargs)
            return wrapper


# Initialize our global container
ioc = Container()