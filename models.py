import sqlalchemy as sa

# Метаданные - это "чертежная доска", где хранятся все таблицы
metadata = sa.MetaData()

# 1. Таблица users
users_table = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(50), nullable=False, unique=True),
    sa.Column("email", sa.String(100), nullable=False),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
)

# 2. Таблица workouts (родительская)
workouts_table = sa.Table(
    "workouts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),  # ... тут все верно, оставляем
        nullable=False,
    ),
    sa.Column("type", sa.String(20), nullable=False),
    sa.Column("started_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("notes", sa.Text, nullable=True),
    sa.CheckConstraint("type IN ('cardio', 'strength')", name="workouts_type_check"),
)

# 3. Таблица cardio_details
cardio_details_table = sa.Table(
    "cardio_details",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "workout_id",
        sa.Integer,
        sa.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # Гарантирует связь 1-к-1
    ),
    sa.Column("distance_meters", sa.Integer, nullable=False),
    sa.Column("duration_seconds", sa.Integer, nullable=False),
    sa.Column("avg_heart_rate", sa.Integer, nullable=True),
    sa.Column("pace_min_per_km", sa.Integer, nullable=True),
)

# 4. Таблица strength_exercises
strength_exercises_table = sa.Table(
    "strength_exercises",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "workout_id",
        sa.Integer,
        sa.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("exercise_name", sa.String(100), nullable=False),
    sa.Column("order", sa.Integer, nullable=False),
)

# 5. Таблица exercise_sets
exercise_sets_table = sa.Table(
    "exercise_sets",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "strength_exercises_id",
        sa.Integer,
        sa.ForeignKey("strength_exercise.id", ondelete="CASCADE"),
    ),
    sa.Column("set_number", sa.Integer, nullable=False),
    sa.Column(
        "weight_kg", sa.Float, nullable=True
    ),  # Может быть NULL для упражнений с собственным весом
    sa.Column("reps", sa.Integer, nullable=False),
)
