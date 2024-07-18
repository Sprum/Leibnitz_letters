from pathlib import Path
from typing import List

import pandas as pd

from aggregate.letter_map import places_set, cities, countries, nationalities_ethnicities, misc, rivers, regions, \
    landmarks, continents, water_bodies


def concat_geocoded_dfs(paths: List[Path]):
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df


if __name__ == '__main__':
    paths = [path for path in Path("./coded").iterdir() if path.suffix == ".csv"]
    sets = [cities, countries, nationalities_ethnicities, misc, rivers, regions, landmarks, continents, water_bodies]

    cdf = concat_geocoded_dfs(paths)
    unique_places = set(cdf['original_Place'])

    for s in sets:
        unique_places -= s

    print(unique_places)
