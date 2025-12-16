from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.scheduler.scheduler import create_scheduler
from app.scraper.scrape_all import scrape_all_cars


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = create_scheduler()
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(
    title="AutoRia Scraper",
    lifespan=lifespan,
)


@app.post("/run-scraper")
async def run_scraper():
    await scrape_all_cars()
    return {"status": "ok"}
