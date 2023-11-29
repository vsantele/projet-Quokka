from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from app.utils.settings import settings


class NeuralSearcher:
    def __init__(self, collection_name=settings.qdrant_collection):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device=settings.device,
        )
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(
            settings.qdrant_host, port=settings.qdrant_port
        )

    def __del__(self):
        """Close the connection to qdrant_client when the class is deleted."""
        self.qdrant_client.close()

    def init_poi(self, pos: list[int], neg: list[int], limit: int = 5):
        """
        Initialize the collection with positive and negative vector ids.

        Args:
            pos (list[int]): List of positive vector ids.
            neg (list[int]): List of negative vector ids.

        Returns:
            list: List of payloads associated with the closest vectors found.
        """
        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.recommend(
            collection_name=self.collection_name,
            positive=pos,
            negative=neg,
            strategy=models.RecommendStrategy.BEST_SCORE,
            query_filter=models.Filter(
                must_not=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(
                            value="amenity",
                        ),
                    ),
                    models.IsNullCondition(
                        is_null=models.PayloadField(
                            key="image",
                        )
                    ),
                ],
            ),
            limit=limit,
        )
        # `search_result` contains found vector ids with similarity scores
        # along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result if hit.payload is not None]
        return payloads

    def search(
        self,
        pos: list[int],
        neg: list[int],
        around: tuple[float, float],
        radius: float = 1000.0,
        limit: int = 5,
    ):
        """
        Search for closest vectors in the collection based on positive
        and negative vectors, within a specified geographical radius.

        Args:
            pos (list[int]): List of positive vector ids.
            neg (list[int]): List of negative vector ids.
            around (tuple[float, float]): Tuple of latitude (0) and longitude (1) representing the center of the search radius.
            radius (float, optional): Radius of the search area in meters. Defaults to 1000.0.

        Returns:
            list: List of payloads associated with the closest vectors found.
        """
        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.recommend(
            collection_name=self.collection_name,
            positive=pos,
            negative=neg,
            strategy=models.RecommendStrategy.BEST_SCORE,
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
            limit=limit,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores
        # along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result if hit.payload is not None]
        return payloads
