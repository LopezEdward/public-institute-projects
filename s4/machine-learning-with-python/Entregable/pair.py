class Pair:
    def __init__(self, key:int, value:object):
        self.__key = key
        self.__value = value

    def get_key (self) -> int:
        return self.__key
    
    def get_value (self) -> object:
        return self.__value
    
    def set_key (self, new_key:int) -> None:
        if not isinstance(new_key, int):
            raise ValueError()
        
        self.__key = new_key

    def __str__(self) -> str:
        return f"Pair[key={self.__key},value={self.__value}]"
    
class PairGenerator:
    __generator_id_counter:int = 0

    def __init__(self, initial_value:int = 1):
        self.__counter:int = initial_value
        self.generator_uid:int = PairGenerator.__generator_id_counter

        PairGenerator.__generator_id_counter += 1

    def createPair (self, value:object) -> Pair:
        value_i = self.__counter
        self.__counter += 1

        return Pair(value_i, value)
    
    def createPairs (self, values:list[object]) -> list[Pair]:
        pairs:list[Pair] = []
        
        for elem in values:
            pairs.append(self.createPair(elem))

        return pairs

class PairCollection:
    def __init__ (self, pair_generator:PairGenerator = None):
        if not isinstance(pair_generator, PairGenerator):
            raise ValueError()
        
        self.__pair_generator:PairGenerator = pair_generator
        self.__elements:list[Pair] = []

    def hasGenerator (self) -> bool:
        return True if self.__pair_generator != None else False
    
    def generatePair (self, value:object, return_pair:bool = False) -> Pair|None:
        if not self.hasGenerator():
            raise ValueError()
        
        pair:Pair = self.__pair_generator.createPair(value)
        self.addPair(pair)

        return pair if return_pair else None
    
    def generatePairs (self, values:list[object], return_pairs:bool = False) -> list[Pair]|None:
        if not self.hasGenerator():
            raise ValueError()
        
        pairs:list[Pair] = self.__pair_generator.createPairs(values)

        self.addAllPairs(pairs)

        return pairs if return_pairs else None

    def getPair(self, index:int) -> Pair:
        return self.__elements[index]

    def addPair (self, pair:Pair) -> None:
        if not isinstance(pair, Pair):
            raise ValueError()
        
        self.__elements.append(pair)

    def addAllPairs (self, pair_list:list[Pair]) -> None:
        for elem in pair_list:
            self.addPair(elem)

    def removePair(self, pair:Pair) -> None:
        if not isinstance(pair, Pair):
            raise ValueError()
        
        self.__elements.remove(pair)

    def setPairInPosition (self, pair:Pair, position:int) -> None:
        if not isinstance(pair, Pair):
            raise ValueError()
        
        if not isinstance(position, int):
            raise ValueError()
        
        self.__elements[position] = pair

    def replacePair(self, old_pair:Pair, new_pair:Pair) -> None:
        if not isinstance(old_pair, Pair) or not isinstance(new_pair, Pair):
            raise ValueError()
        
        for elem in self.__elements:
            if elem == old_pair:
                elem = new_pair

    def getAllElements (self) -> list[Pair]:
        return self.__elements
    
    def __str__(self) -> str:
        tmp:str = "PairCollection["

        for index in range(len(self.__elements)):
            if index + 1 == len(self.__elements):
                tmp += self.__elements[index].__str__()
                continue
            
            tmp += self.__elements[index].__str__() + ", "

        tmp += "]"

        return tmp