DEFAULT_PROFILE = {
    "nazev": "Omega facilities s.r.o.",
    "obory": [
        "stavební práce",
        "rekonstrukce",
        "správa nemovitostí",
        "facility management",
        "dodávky stavebního materiálu",
    ],
    "max_hodnota_zakazky_czk": 10_000_000,
    "geografie": ["Česká republika"],
    "certifikace": [],
    "reference": [
        "rekonstrukce bytového domu",
        "správa SVJ",
        "stavební práce pro soukromé investory",
    ],
    "rocni_obrat_czk": 5_000_000,
}

def get_profile() -> dict:
    return DEFAULT_PROFILE