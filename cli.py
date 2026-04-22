import asyncio
import argparse
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
url = os.getenv("DATABASE_URL")

engine = create_async_engine(url)


async def add_user(username: str, email: str):
    """Добавляет пользователя и его email"""
    t = text(
        "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    )
    async with engine.connect() as conn:
        result = await conn.execute(t, {"username": username, "email": email})
        user_id = result.scalar_one()
        await conn.commit()  # ← обязательно комитить
        print(f"✅ Пользователь создан с ID: {user_id}")


async def add_cardio_workout(
    username: str,
    distance: float,  # метры
    duration: int,  # секунды
    notes: str | None = None,
    avg_heart_rate: int | None = None,
    pace_min_per_km: int | None = None,
):
    """Добавляет кардио-тренировку для пользователя."""
    async with engine.connect() as conn:
        # 1. Проверяем существование пользователя
        user_select = text("SELECT id FROM users WHERE username = :username")
        result = await conn.execute(user_select, {"username": username})
        user_id = result.scalar_one_or_none()

        if user_id is None:
            print(f"❌ Пользователь '{username}' не найден.")
            return  # не уверен правильно ли возврат идет, надо проверить

        # 2. Вставляем в workouts
        workout_insert = text("""
            INSERT INTO workouts (user_id, type, notes)
            VALUES (:user_id, 'cardio', :notes)
            RETURNING id
        """)
        result = await conn.execute(
            workout_insert, {"user_id": user_id, "notes": notes}
        )
        workout_id = result.scalar_one()

        # 3. Вставляем в cardio_details
        cardio_insert = text("""
            INSERT INTO cardio_details
                (workout_id, distance_meters, duration_seconds, avg_heart_rate, pace_min_per_km)
            VALUES
                (:workout_id, :distance, :duration, :avg_hr, :pace)
        """)
        await conn.execute(
            cardio_insert,
            {
                "workout_id": workout_id,
                "distance": distance,
                "duration": duration,
                "avg_hr": avg_heart_rate,
                "pace": pace_min_per_km,
            },
        )

        # 4. Фиксируем транзакцию
        await conn.commit()

        print(f"✅ Кардио-тренировка добавлена (ID: {workout_id})")
        print(f"   Дистанция: {distance} м, Длительность: {duration} сек")


async def main():
    parser = argparse.ArgumentParser(description="Workout Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда add-user
    parser_add = subparsers.add_parser("add-user", help="Добавить пользователя")
    parser_add.add_argument("username", type=str, help="Имя пользователя")
    parser_add.add_argument("email", type=str, help="Электронная почта")

    args = parser.parse_args()

    if args.command == "add-user":
        await add_user(args.username, args.email)


if __name__ == "__main__":
    asyncio.run(main())
