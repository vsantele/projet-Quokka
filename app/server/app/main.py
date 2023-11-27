from fastapi import FastAPI
from app.models.search_nearby import SearchNearbyBody
from app.services.neural_searcher import NeuralSearcher
from app.services.profils import get_profil

app = FastAPI()

ns = NeuralSearcher(collection_name="poi")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/nearby")
async def nearby(request: SearchNearbyBody):
    profile = get_profil(request.profil)
    if profile is None:
        return {"error": "profil not found"}
    default_pos = profile.pos
    default_neg = profile.neg
    pos = default_pos + request.pos
    neg = default_neg + request.neg
    print(pos, neg)
    res = ns.search(pos=pos, neg=neg, around=(request.lat, request.lon))
    return res
