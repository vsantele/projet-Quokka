import numpy as np
import polars as pl
from qdrant_client import QdrantClient, models


def add_loc(row):
    row["location"] = {"lat": row["lat"], "lon": row["lon"]}
    return row


df_geo = pl.read_parquet("./data/transformed/poi_clean_category_geo.parquet")
df = df_geo.drop(["type", "geometry"])

client = QdrantClient("localhost", port=6333)
vectors = np.load("./poi_vectors.npy", allow_pickle=False)

client.recreate_collection(
    collection_name="poi",
    vectors_config=models.VectorParams(
        size=vectors.shape[1],
        distance=models.Distance.COSINE,
    ),
)


client.upload_collection(
    collection_name="poi",
    vectors=vectors,
    payload=[add_loc(row) for row in df.to_dicts()],
    ids=df["id"].to_list(),
    batch_size=256,
)
