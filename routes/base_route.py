from abc import abstractmethod
from typing import Any, Protocol


class BaseRoute(Protocol):
    __path: str
    __methods_types: list[str] | None
    
    
    @property
    def methods_type(self):
        return self.__methods_types
    
    @methods_type.setter
    def methods_type(self, *v: str):
        if getattr(self, "__methods_types", None) is None:
            self.__methods_types = [*v,]
        elif self.__methods_types is not None:
            for method in v:
                self.__methods_types.append(method)

    @methods_type.deleter
    def methods_type(self):
        del self.__methods_types

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, v: str):
        if v[0] != '/':
            self.__path = f"/{v}"
        else:
            self.__path = v

    @abstractmethod
    def endpoint(self, *args, **kwargs) -> Any: ...