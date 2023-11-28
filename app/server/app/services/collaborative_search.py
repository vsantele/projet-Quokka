import pickle
from surprise import SVD


class CollaborativeSearch:
    def __init__(self) -> None:
        file = open("./data/algoSVD.pkl", "rb")
        self.model = pickle.load(file)
        file.close()
