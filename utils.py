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


def validate_strength_workout(data: dict) -> dict:
    # exercises - непустой список
    exercises = data.get("exercises", [])
    if not exercises:
        raise ValueError("exercises list must not be empty")

    # Для КАЖДОГО exercise в exercises:
    for exercise in exercises:
        # Проверить, что имя не пустое
        name = exercise.get("name", "")
        if not name.strip():
            raise ValueError("exercise name must not be empty")

        # Проверить, что sets - непустой список
        sets = exercise.get("sets", [])
        if not sets:
            raise ValueError("sets must not be empty")  # позже добавить

        # Для КАЖДОГО set в sets:
        for s in sets:
            # Проверить вес
            if s.get("weight", 0) < 0:
                raise ValueError("weight must not be negative")
            # Проверить повторения
            if s.get("reps", 0) <= 0:
                raise ValueError("reps must be greater than 0")

    # Вернуть data (пока без нормализации)
    return data
