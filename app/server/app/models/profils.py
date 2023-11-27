from enum import Enum


class Profils(Enum):
    nature = "nature"
    history_medieval = "history_medieval"
    monument = "monument"
    history_19_20 = "history_19_20"
    artistic = "artistic"
    antiquity = "antiquity"
    museum = "museum"
    history = "history"
    religious = "religious"


class Profil:
    def __init__(
        self,
        id_profil: Profils,
        name: str,
        pos: list[int],
        neg: list[int],
    ):
        self.id_profil = id_profil
        self.name = name
        self.pos = pos
        self.neg = neg
