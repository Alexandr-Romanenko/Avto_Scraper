import asyncio
import aiohttp

from app.config.settings import settings
from app.db.database import async_session_factory
from app.crud.crud import save_car
from app.scraper.fetch import fetch
from app.scraper.fetch_phone import PhoneClient
from app.scraper.parse import parse_base_car_info
from app.scraper.scrape_car import CarDetailScraper


async def scrape_all_cars(concurrent_requests: int = settings.app.concurrent_requests):
    sem = asyncio.Semaphore(concurrent_requests)
    timeout = aiohttp.ClientTimeout(
            total=30,
            connect=10,
            sock_read=20,
        )

    async with aiohttp.ClientSession(
        timeout=timeout,
        headers={"User-Agent": settings.app.user_agent},
        cookies=settings.app.cookies,
    ) as http, PhoneClient(settings.app.cookies) as phone_client:

        scraper = CarDetailScraper(http, phone_client)

        page = 0
        while True:
            list_url = (
                settings.app.start_url
                if page == 0
                else f"https://auto.ria.com/uk/search/?indexName=auto&page={page}"
            )

            html = await fetch(http, list_url)
            if not html:
                break

            cars = parse_base_car_info(html)
            if not cars:
                  break

            async def worker(car):
                async with sem:
                    car_create = await scraper.scrape(car)
                    if car_create:
                        async with async_session_factory() as db:
                            await save_car(db, car_create)
                            await db.commit()

            await asyncio.gather(*(worker(car) for car in cars))

            page += 1
