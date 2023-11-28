from pydantic import BaseModel

from app.models.profils import Profils


class UserInteraction(BaseModel):
    uid: str
    profil_id: Profils
    poi_id: int
    rating: float
    timestamp: int
