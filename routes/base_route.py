from abc import abstractmethod
from typing import Protocol


class BaseRoute(Protocol):
    __path: str
    __methods_types: list[str] | None
    
    
    @property
    def methods_type(self):
        return self.__methods_types
    
    @methods_type.setter
    def methods_type(self, *v: str):
        if self.__methods_types is None:
            self.__methods_types = [*v,]
        else:
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
        if v[0] is not '/':
            self.__path = f"/{v}"
        else:
            self.__path = v

    @abstractmethod
    def endpoint(self): ...