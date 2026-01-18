from dataclasses import dataclass
@dataclass
class Category:
    id: int
    category_name: str

    def __str__(self):
        return f'Categoria: {self.id} {self.category_name}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
