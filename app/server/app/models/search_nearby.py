from pydantic import BaseModel
from app.services.profils import Profils


class SearchNearbyBody(BaseModel):
    lat: float
    lon: float
    radius: float = 1000.0
    profil: Profils
    pos: list[int] = []
    neg: list[int] = []
