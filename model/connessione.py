from dataclasses import dataclass
@dataclass
class Connessione:
    id_rifugio1:int
    id_rifugio2:int
    distanza:float
    difficolta:str