"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    # TODO: use csv.DictReader to read csv_path into a list of dicts.
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        study_spots = []
        for row in reader:
            # Convert distance_miles to float and seats_available to int
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            study_spots.append(row)
    return study_spots



def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    # TODO: implement additive/weighted scoring using at least noise_level
    # (compare using NOISE_ORDER), distance_miles vs max_distance, and
    # seats_available vs min_seats. Append a short string to `reasons` for
    # each factor that contributed, whether it helped or hurt the score.

    #NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}
    score = 0
    reasons = []
    #Scoring will reward those that match the profile.
    
    #1. Reward spots that have enough seats with +10
    if spot["seats_available"] >= profile["min_seats"]:
        score += 10
        reasons.append(f"Enough seats: {spot['seats_available']} seats")
    #2. Reward spots that are close enough with +5
    if spot["distance_miles"] <= profile["max_distance"]:
        #add weighted scoring for distance, closer is better (distance higher score)
        distance_score = (profile["max_distance"] - spot["distance_miles"]) / profile["max_distance"] * 8 if profile["max_distance"] > 0 else 0
        score += distance_score
        if distance_score > 0:
            reasons.append(f"close enough distance: {spot['distance_miles']} miles")
        else:
            reasons.append("too far")
    #3. Reward spots that are not too loud 
    if NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]]:
        #add weighted score for each noise level, quieter is better
        noise_score = (NOISE_ORDER[profile["max_noise"]] - NOISE_ORDER[spot["noise_level"]]) / len(NOISE_ORDER) * 5 if len(NOISE_ORDER) > 0 else 0
        score += noise_score
        if noise_score > 0:
            reasons.append(f"Tolerable Noise Level: {spot['noise_level']}")
        else:
            reasons.append("too loud")

    #round score to 2 
    score = round(score, 2)

    return (score, reasons)



def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    # TODO: score every spot with score_study_spot(), then use
    # sorted(..., key=..., reverse=True)[:k] to keep only the top k.

    for spot in spots:
        score, reasons = score_study_spot(profile, spot)
        spot["score"] = score
        spot["reasons"] = reasons

    # Sort the spots by score in descending order and keep only the top k
    ranked_spots = sorted(spots, key=lambda x: x["score"], reverse=True)[:k]
    #print(f"Ranked spots: {ranked_spots}")  # Debugging print statement
    return ranked_spots


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    # TODO: for each (spot, score, reasons) tuple, print a readable line, e.g.:
    # "1. Innovation Commons -- Score: 5.0 -- Because: quiet enough, close enough"
    for i, spot in enumerate(ranked, start=1):
        print(f"{i}. {spot['name']} -- Score: {spot['score']:.1f} -- Because: {', '.join(spot['reasons'])}")


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    # print(load_study_spots("data/study_spots.csv"))
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
