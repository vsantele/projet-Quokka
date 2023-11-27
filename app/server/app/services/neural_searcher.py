import torch
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("localhost", port=6333)

    def search(
        self,
        pos: list[int],
        neg: list[int],
        around: tuple[float, float],
        radius: float = 1000.0,
    ):
        """
        Search for closest vectors in the collection based on positive
        and negative vectors, within a specified geographical radius.

        Args:
            pos (list[int]): List of positive vector ids.
            neg (list[int]): List of negative vector ids.
            around (tuple[float, float]): Tuple of latitude (0) and longitude (1) representing the center of the search radius.

        Returns:
            list: List of payloads associated with the closest vectors found.
        """
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
                            radius=radius,
                        ),
                    ),
                ],
                must_not=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(
                            value="amenity",
                        ),
                    )
                ],
            ),
            limit=5,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores
        # along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads
