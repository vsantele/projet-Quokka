from fastapi import FastAPI, HTTPException
from app.models.search_nearby import SearchNearbyBody
from app.models.profils import Profil, Profils
from app.utils.settings import settings
from app.services.neural_searcher import NeuralSearcher
from app.services.profils import get_profil, get_profiles

app = FastAPI()

ns = NeuralSearcher(collection_name=settings.qdrant_collection)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/nearby")
async def nearby(request: SearchNearbyBody):
    profile = get_profil(request.profil)
    if profile is None:
        raise HTTPException(status_code=400, detail="Profil not found")
    default_pos = profile.pos
    default_neg = profile.neg
    pos = default_pos + request.pos
    neg = default_neg + request.neg
    res = ns.search(
        pos=pos,
        neg=neg,
        around=(request.lat, request.lon),
        radius=request.radius,
    )
    return res


@app.get("/profils", response_model=list[Profil])
async def profils():
    return get_profiles()


@app.get("/init")
async def init(profil_id: Profils):
    profil = get_profil(profil_id)
    init_pois = ns.init_poi(pos=profil.pos, neg=profil.neg)
    return init_pois
