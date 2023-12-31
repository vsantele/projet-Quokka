from ..models.profils import Profil, Profils


def get_profiles() -> list[Profil]:
    return [
        Profil(
            id_profil=Profils.nature,
            name="Fan de la nature",
            pos=[
                161902431,
                6256757776,
                5771053254,
                8731063849,
                9609413254,
                8615466894,
                9356148774,
                304351397,
                304374138,
            ],
            neg=[
                304850843,
                9964615559,
                6264550437,
                2514192427,
                11186120804,
                9663434784,
            ],
        ),
        Profil(
            id_profil=Profils.history_medieval,
            name="Historique (médieval)",
            pos=[
                9964615559,
                2080454089,
                8309291920,
                9767828163,
                10815282268,
                11006240930,
                6635074831,
                205161375,
                312031207,
                9964615559,
            ],
            neg=[267878387, 6264550437, 6256757776, 304882303, 310235557],
        ),
        Profil(
            id_profil=Profils.monument,
            name="Monument typique (Grand lieu)",
            pos=[6580307576, 249292417, 267878387],
            neg=[8731063849, 8731063849, 6635074831, 9767828163],
        ),
        Profil(
            id_profil=Profils.history_19_20,
            name="Historique (19,20ème)",
            pos=[
                267878387,
                6264550437,
                2514258897,
                2084125343,
                407714718,
                34050681,
                271394429,
                310235557,
                368996291,
                393969161,
            ],
            neg=[
                312415707,
                291231959,
                9356148774,
                11186120804,
                6256757776,
                34050692,
                304374138,
            ],
        ),
        Profil(
            id_profil=Profils.artistic,
            name="Artistique",
            pos=[
                2514192427,
                9663434784,
                251316201,
                11186120804,
                291231959,
            ],
            neg=[
                9356148774,
                407714718,
                11006240930,
                9964615559,
                310235557,
                393969161,
            ],
        ),
        Profil(
            id_profil=Profils.antiquity,
            name="Antiquité",
            pos=[4729709152, 874341418, 9864187809, 34050692],
            neg=[267878387, 9609413254, 271394429, 6635074831, 6580307576],
        ),
        Profil(
            id_profil=Profils.museum,
            name="Fan de musée",
            pos=[
                34050681,
                393969161,
                34050692,
                160079640,
                251316201,
                252382829,
                291231959,
                311512162,
                34050692,
            ],
            neg=[9609413254, 6580307576, 2084125343, 407714718],
        ),
        Profil(
            id_profil=Profils.history,
            name="Histoire (général)",
            pos=[
                251316201,
                252382829,
                258816379,
                291232006,
                304882303,
                310235557,
            ],
            neg=[6256757776, 5771053254, 2514192427, 6580307576],
        ),
        Profil(
            id_profil=Profils.religious,
            name="Religieux",
            pos=[
                251466390,
                304850843,
                307675986,
                304850843,
            ],
            neg=[251316201],
        ),
        Profil(id_profil=Profils.other, name="Autre", pos=[], neg=[]),
    ]


def get_profil(id_profil: Profils):
    profiles = get_profiles()
    return next(
        (profil for profil in profiles if profil.id_profil == id_profil),
        None,
    )


def get_names():
    profiles = get_profiles()
    return [profil.name for profil in profiles]
