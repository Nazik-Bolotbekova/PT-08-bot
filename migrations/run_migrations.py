import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
# 📁 Путь к миграциям
MIGRATIONS_DIR = "migrations"

# 🔧 Настройки подключения
DB_SETTINGS = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


async def ensure_migrations_table(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            filename TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT NOW()
        )
    """)


async def get_applied_migrations(conn) -> set:
    rows = await conn.fetch("SELECT filename FROM migrations")
    return {row["filename"] for row in rows}


async def apply_migration(conn, filename, sql_content):
    async with conn.transaction():
        await conn.execute(sql_content)
        await conn.execute("INSERT INTO migrations(filename) VALUES ($1)", filename)


async def run_migrations():
    conn = await asyncpg.connect(**DB_SETTINGS)
    try:
        await ensure_migrations_table(conn)
        applied = await get_applied_migrations(conn)

        files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

        for file in files:
            if file in applied:
                print(f"✅ Уже применено: {file}")
                continue

            path = os.path.join(MIGRATIONS_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                sql_content = f.read()

            print(f"🚀 Применение миграции: {file}")
            try:
                await apply_migration(conn, file, sql_content)
                print(f"✅ Успешно: {file}")
            except Exception as e:
                print(f"❌ Ошибка в {file}: {e}")
                break
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run_migrations())