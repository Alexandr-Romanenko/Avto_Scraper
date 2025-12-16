import os
import subprocess
import traceback

from datetime import datetime
from app.config.settings import settings
from app.scraper.scrape_all import scrape_all_cars
from pathlib import Path

async def scrape_job():
    try:
        print("Scraping all cars")
        await scrape_all_cars()
    except Exception:
        print("Scrape job failed")
        traceback.print_exc()

def dump_db_job():
    dumps_dir: Path = settings.app.dumps_path  # должно быть Path, например Path("./dumps")
    dumps_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    dump_file = dumps_dir / f"dump_{date_str}.sql"

    # Формируем команду pg_dump
    cmd = [
        "pg_dump",
        "-h", settings.db.host,
        "-p", str(settings.db.port),
        "-U", settings.db.user,
        settings.db.db
    ]

    # Открываем файл и пишем туда stdout команды
    try:
        with open(dump_file, "wb") as f:
            subprocess.run(cmd, check=True, stdout=f, env={
                **dict(**os.environ),  # передаем существующие переменные окружения
                "PGPASSWORD": settings.db.password  # чтобы не вводить пароль вручную
            })
        print(f"Dump saved to {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to dump DB: {e}")

# def dump_db_job():
#     dumps_dir = settings.app.dumps_path
#     date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
#     dump_file = dumps_dir / f"dump_{date_str}.sql"
#
#     cmd = [
#         "pg_dump",
#         settings.db.pg_dump_url,
#         "-f",
#         str(dump_file),
#     ]
#
#     subprocess.run(cmd, check=True)
