from neural_searcher import NeuralSearcher
from profils import get_profiles

# Initialize searcher
searcher = NeuralSearcher(collection_name="poi")

namur = [50.465, 4.867]
mons = [50.454, 3.952]
liege = [50.633, 5.567]
mouscron = [50.733, 3.233]

# Get profiles
df_profil = get_profiles()

first_profile = df_profil[0]

# Search for the first profile
search_result = searcher.search(
    pos=first_profile["pos"], neg=first_profile["neg"], around=namur
)

# Print the first result
print(
    [
        [
            res.get("id"),
            res.get("name"),
            res.get("category"),
            res.get("sub_category"),
        ]
        if res is not None
        else "None"
        for res in search_result
    ]
)
