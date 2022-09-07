def estimate_time(version, potential_rosters):
    if version == "low":
        return round(potential_rosters / 3000000, 2)
    elif version == "high":
        return round(potential_rosters / 500000 * 4, 2)


def get_time(start, end):
    return str(round(end - start, 2))
