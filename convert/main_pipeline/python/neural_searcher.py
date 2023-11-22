import torch
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"


qdrant_path = "./data/transformed/qdrant"


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(path=qdrant_path)
        self.radius = 1000.0

    def search(self, pos, neg, around):
        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.recommend(
            collection_name=self.collection_name,
            positive=pos,
            negative=neg,
            strategy=models.RecommendStrategy.AVERAGE_VECTOR,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="location",
                        geo_radius=models.GeoRadius(
                            center=models.GeoPoint(
                                lon=around[1],
                                lat=around[0],
                            ),
                            radius=self.radius,
                        ),
                    ),
                ],
                # must_not=[
                #     models.FieldCondition(
                #         key="category",
                #         match=models.MatchValue(
                #             value="amenity",
                #         ),
                #     )
                # ],
            ),
            limit=5,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores
        # along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads
