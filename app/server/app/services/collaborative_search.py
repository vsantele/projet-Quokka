import pickle
from surprise import SVD


class CollaborativeSearch:
    def __init__(self) -> None:
        with open("./data/algoSVD.pkl", "rb") as file:
            self.model: SVD = pickle.load(file)

    def predict(self, uid: str, poi_id: int) -> float:
        return self.model.predict(uid, poi_id).est
