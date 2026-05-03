def parse_pace(pace_str: str) -> int:
    parts = pace_str.split(":")
    if len(parts) == 1:
        return int(parts[0]) * 60
    elif len(parts) == 2:
        minutes, seconds = int(parts[0]), int(parts[1])
        if not (0 <= seconds < 60):
            raise ValueError("Seconds must be 0-59")
        return (minutes * 60) + seconds
    else:
        raise ValueError("Invalid pace format. Use 'MM:SS' or 'MM'")


def validate_strength_workout():
    pass
