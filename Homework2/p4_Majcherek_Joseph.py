"""Problem 4: IMDB Top Rated & Highest Grossing Movie Analytics.

Parses IMDB dataset CSV files to identify director-actor collaboration totals
and compute box-office earnings per actor.
"""

from typing import List, Tuple, Set, Dict
import csv
import os

def read_imdb_casts(filename: str) -> List[Tuple[str, str, str, List[str]]]:
    """Read the top casts CSV file (Title, Year, Director, Actor1..Actor5)."""
    casts = []
    with open(filename, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not row or len(row) < 4:
                continue
            title = row[0].strip()
            year = row[1].strip()
            director = row[2].strip()
            actors = [actor.strip() for actor in row[3:] if actor.strip()]
            casts.append((title, year, director, actors))
    return casts

def read_top_rated(filename: str) -> Set[Tuple[str, str]]:
    """Read Top-Rated CSV and return a set of (Title, Year) keys."""
    read_top_keys = set()
    with open(filename, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader, None) #Skip header
        for row in reader:
            if row:
                read_top_keys.add((row[1].strip(), row[2].strip()))
    return read_top_keys

def read_top_grossing(filename: str) -> Dict[Tuple[str, str], float]:
    """Read Top-Grossing CSV and return dict mapping (Title, year) -> BoxOffice."""
    grossing_dict = {}
    with open(filename, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader, None)
        for row in reader:
            if row:
                title = row[1].strip()
                year = row[2].strip()
                # Parse gross income (stripping '$' or commas if present)
                raw_box = row[3].replace('$', '').replace(',', '').strip()
                grossing_dict[(title, year)] = float(raw_box)
    return grossing_dict

def display_top_collaborations(casts_file: str, top_rated_file: str, limit: int = 10) -> None:
    """Display ranking of (Director, Actor) pairs by total top-rated movie collaborations."""
    top_rated_set = read_top_rated(top_rated_file)
    casts = read_imdb_casts(casts_file)

    collab_counts = {}
    for title, year, director, actors in casts:
        if (title, year) in top_rated_set:
            for actor in actors:
                pair = (director, actor)
                collab_counts[pair] = collab_counts.get(pair, 0) + 1

    sorted_collabs = sorted(collab_counts.items(), key=lambda item: item[1], reverse=True)

    print(f"\n--- Top {limit} Director-Actor Collaborations (Top-Rated Movies) ---")
    print(f"{'Rank':<5} {'Director':<25} {'Actor':<25} {'Movies':<6}")
    print("-" * 65)
    for idx, ((director, actor), count) in enumerate(sorted_collabs[:limit], start=1):
        print(f"{idx:<5} {director:<25} {actor:<25} {count:<6}")

def display_top_actors(casts_file: str, top_grossing_file: str, limit: int = 10) -> None:
    """Display ranking of actors ordered by cumulative box-office gross of their films."""
    grossing_dict = read_top_grossing(top_grossing_file)
    casts = read_imdb_casts(casts_file)

    actor_earnings = {}
    for title, year, _, actors in casts:
        if (title, year) in grossing_dict:
            box_office = grossing_dict[(title, year)]
            for actor in actors:
                actor_earnings[actor] = (
                    actor_earnings.get(actor, 0.0) + box_office
                )

    sorted_actors = sorted(actor_earnings.items(), key=lambda item: item[1], reverse=True)

    print(f"\n--- Top {limit} Actors by Cumulative USA Box Office Gross ---")
    print(f"{'Rank':<5} {'Actor':<30} {'Total Box Office ($)':<20}")
    print("-" * 60)
    for idx, (actor, total_gross) in enumerate(sorted_actors[:limit], start=1):
        print(f"{idx:<5} {actor:<30} ${total_gross:,.2f}")

def main() -> None:
    """Main execution function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    casts_file = os.path.join(script_dir, "imdb-top-casts.csv")
    top_rated_file = os.path.join(script_dir, "imdb-top-rated.csv")
    top_grossing_file = os.path.join(script_dir, "imdb-top-grossing.csv")

    display_top_collaborations(casts_file, top_rated_file, limit=10)
    display_top_actors(casts_file, top_grossing_file, limit=10)

if __name__ == "__main__":
    main()