import polars as pl

df = pl.read_parquet("data\\transformed\\poi_clean_category.parquet")

df_add = pl.read_csv("data\\transformed\\musee_et_sites.csv", separator=";")

max_id = df.select(pl.col("id")).max().item() + 1
df_id = pl.DataFrame(
    {
        "type": ["node" for _ in range(len(df_add))],
        "id": range(max_id, max_id + len(df_add)),
    }
)

df_add = pl.concat([df_id, df_add], how="horizontal")
df_concat = pl.concat([df, df_add], how="vertical_relaxed")

df_concat.select(
    [
        pl.col("id"),
        pl.col("name"),
        pl.col("category"),
        pl.col("sub_category"),
        pl.col("addr:city").alias("city"),
        pl.col("addr:postcode").alias("postcode"),
        pl.col("addr:street").alias("street"),
        pl.col("addr:housenumber").alias("housenumber"),
        pl.col("alt_name"),
        pl.col("brand"),
        pl.col("contact:email").alias("email"),
        pl.col("contact:facebook").alias("facebook"),
        pl.col("contact:mobile").alias("mobile"),
        pl.col("contact:phone").alias("phone"),
        pl.col("contact:website").alias("website"),
        pl.col("description"),
        pl.col("image"),
        pl.col("internet_access"),
        pl.col("lat"),
        pl.col("lon"),
        pl.col("opening_hours"),
        pl.col("operator"),
        pl.col("old_name"),
        pl.col("wheelchair"),
        pl.col("wikipedia"),
        pl.col("wikidata"),
        pl.col("url"),
    ]
).write_parquet("data\\transformed\\poi_clean_category_all.parquet")
