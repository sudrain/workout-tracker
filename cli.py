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
    t = text(
        "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    )
    async with engine.connect() as conn:
        result = await conn.execute(t, {"username": username, "email": email})
        user_id = result.scalar_one()
        await conn.commit()  # ← обязательно комитить
        print(f"✅ Пользователь создан с ID: {user_id}")


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
