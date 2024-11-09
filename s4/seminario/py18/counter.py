from typing import Iterable

class Counter:
    def __init__ (self):
        self.__map:dict[object, int] = dict()

    def count_value(self, value:object) -> None:
        if not value in self.__map.keys():
            self.__map[value] = 0

        self.__map[value] += 1

    def count_values(self, values:Iterable[object]) -> None:
        for value in values:
            self.count_value(value)

    def counter_of_values (values:Iterable[object]):
        counter:Counter = Counter()
        counter.count_values(values)

        return counter

    def get_count(self, value:object) -> int:
        if not value in self.__map.keys():
            return 0

        return self.__map[value]

    def get_count_object(self) -> tuple[object]:
        return tuple([x for x in self.__map.keys()])

    def get_value_count_object (self) -> tuple[int]:
        return tuple([x for x in self.__map.values()])

    def __str__(self) -> str:
        return f"Counter[{self.__map.__str__()}]"
            

    