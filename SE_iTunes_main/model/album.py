from dataclasses import dataclass
@dataclass
class Album:
    id : int
    title : str
    artist_id : int

    def __str__(self) -> str:
        return f'Album: {self.id}, {self.title}, {self.artist_id}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)