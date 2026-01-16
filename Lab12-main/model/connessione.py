from dataclasses import dataclass
@dataclass
class Connessione:
    id : int
    id_rifugio1: int
    id_rifugio2: int
    distanza:float
    difficolta:str
    durata:str
    anno:int

    def __str__(self):
        return f"Sentiero: {self.id_rifugio1}, {self.id_rifugio2}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)