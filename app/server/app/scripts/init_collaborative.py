import math
import os

import polars as pl
from ..models.profils import Profils
from surprise import SVD, Dataset, Reader

from ..models.user_interaction import UserInteraction
from ..services.profils import get_profiles
from nanoid import generate
import random
import time
import pickle

random.seed(42)


def get_random_pois(pois: list[int]):
    pois_len = len(pois)
    if pois_len == 0:
        return []
    if pois_len < 3:
        return pois
    return random.sample(
        pois,
        random.randint(
            max(math.ceil(pois_len * 0.2), 2),
            pois_len,
        ),
    )


def get_users(nb: int) -> list[tuple[str, Profils, list[int], list[int]]]:
    users = []
    for _ in range(nb):
        prof = random.choice(get_profiles())
        user = (
            generate(),
            prof.id_profil,
            get_random_pois(prof.pos),
            get_random_pois(prof.neg),
        )
        users.append(user)
    return users


def get_user_interactions(
    user: tuple[str, Profils, list[int], list[int]]
) -> list[UserInteraction]:
    user_interactions = []
    current_timestamp = int(time.time())
    for pos in user[2]:
        user_inter = UserInteraction(
            uid=user[0],
            profil_id=user[1],
            poi_id=pos,
            rating=1,
            timestamp=current_timestamp + random.randint(-1000, 1000),
        )
        user_interactions.append(user_inter)
    for neg in user[3]:
        user_inter = UserInteraction(
            uid=user[0],
            profil_id=user[1],
            poi_id=neg,
            rating=0,
            timestamp=current_timestamp + random.randint(-1000, 1000),
        )
        user_interactions.append(user_inter)
    return user_interactions


profiles = get_profiles()
users = get_users(50)

user_interactions: list[UserInteraction] = []
for user in users:
    user_interactions.extend(get_user_interactions(user))

reader = Reader(rating_scale=(0, 1))
df_user_interactions = pl.DataFrame(
    [user.model_dump() for user in user_interactions],
)
data = Dataset.load_from_df(
    df_user_interactions.select(
        pl.col("uid"), pl.col("poi_id"), pl.col("rating")
    ).to_pandas(),
    reader,
)

algo = SVD()
algo.fit(data.build_full_trainset())


# Save the algo object to a file
os.makedirs("./data", exist_ok=True)
with open("./data/algoSVD.pkl", "wb") as f:
    pickle.dump(algo, f)
