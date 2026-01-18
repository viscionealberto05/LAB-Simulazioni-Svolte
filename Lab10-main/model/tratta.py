from dataclasses import dataclass
@dataclass
class Tratta:
    id_hub_1 : int
    id_hub_2 : int
    somma_tratta : float
    n_spedizioni : int

    def __str__(self):
        return f"Tratta {self.id_hub_1} - {self.id_hub_2} , Valore: {self.somma_tratta}"

    def __eq__(self, other):
        return self.id_hub_1 == other.id_hub_1 and self.id_hub_2 == other.id_hub_2

    def __hash__(self):
        return hash((self.id_hub_1, self.id_hub_2))