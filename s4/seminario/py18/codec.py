from collections.abc import KeysView, ValuesView
from typing import Iterable

class ClassCodec:
    def __init__ (self):
        self.__counter:int = 0
        self.__map:dict[str, int] = {}
    
    def code (self, value:str) -> int:
        if self.__map.get(value) == None:
            self.__map[value] = self.__counter
            self.__counter += 1
        
        return self.__map[value]

    def decode (self, code:int) -> str:
        # Possibly fatal error => The "code" element exists in map? 
        if self.__map.__len__() == 0:
            raise Exception("No hay elementos para decodificar")

        key_s:str = None

        for key, value in self.__map.items():
            if code == value:
                return key

        raise ValueError("No exists " + code + " in this object!") # I think this is a fatal error

    def code_all (self, array_like:Iterable[str]) -> tuple[int]:
        return tuple([self.code(value) for value in array_like])

    def decode_all (self, array_like:Iterable[int]) -> tuple[str]:
        return tuple([self.decode(value) for value in array_like])

    def get_keys(self, in_tuple:bool = False) -> KeysView[str]|tuple[str]:
        return tuple([x for x in self.__map.keys()]) if in_tuple else self.__map.keys()

    def get_values(self, in_tuple:bool=False) -> ValuesView[int]|tuple[int]:
        return tuple([x for x in self.__map.values()]) if in_tuple else self.__map.values()

    def __dict__(self) -> dict:
        return self.__map

    def __str_(self) -> str:
        return self.__map.__str__()