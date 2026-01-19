from dataclasses import dataclass
@dataclass
class Team:
    id:int
    year:int
    team_code:str
    div1_id:str
    div2_id:int
    team_rank:int
    games:int
    games_home:int
    wins:int
    losses:int
    division_winner:str
    league_winner:str
    world_series_winner:str
    runs:int
    hits:int
    homeruns:int
    stolen_bases:int
    hits_allowed:int
    homeruns_allowed:int
    name:str
    park:str

    def __str__(self):
        return f"Team: {self.id}, {self.year}, {self.team_code}"

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)