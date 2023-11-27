import numpy as np
import polars as pl
import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

encoder = SentenceTransformer("paraphrase-MiniLM-L6-v2", device=device)


def not_null(string: str):
    return string if string else ""


def convert(row):
    return ", ".join(
        [
            "category: " + row["category"],
            "sub_category: " + row["sub_category"],
            "name: " + row["name"],
            "alt_name: " + not_null(row["alt_name"]),
            "description: " + not_null(row["description"]),
        ]
    )


df_geo = pl.read_parquet("./data/transformed/poi_clean_category_geo.parquet")
df = df_geo.drop(["type", "geometry"])
print(df.head())
vectors = encoder.encode(
    [convert(row) for row in df.iter_rows(named=True)],
    batch_size=256,
    show_progress_bar=True,
    device=device,
)


np.save("./poi_vectors.npy", vectors, allow_pickle=False)
