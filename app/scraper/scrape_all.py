import asyncio
import aiohttp

from app.config.settings import settings
from app.db.database import async_session_factory
from app.crud.crud import save_car
from app.scraper.fetch import fetch
from app.scraper.fetch_phone import PhoneClient
from app.scraper.parse import parse_base_car_info
from app.scraper.scrape_car import CarDetailScraper



# async def scrape_all_cars(concurrent_requests: int = settings.app.concurrent_requests):
#     sem = asyncio.Semaphore(concurrent_requests)
#
#     timeout = aiohttp.ClientTimeout(
#         total=30,
#         connect=10,
#         sock_read=20,
#     )
#
#     async with aiohttp.ClientSession(
#         timeout=timeout,
#         headers={"User-Agent": settings.app.user_agent},
#         cookies=settings.app.cookies,
#     ) as http, PhoneClient(settings.app.cookies) as phone_client:
#
#         scraper = CarDetailScraper(http, phone_client)
#
#         page = 0
#         while True:
#             list_url = (
#                 settings.app.start_url
#                 if page == 0
#                 else f"https://auto.ria.com/uk/search/?indexName=auto&page={page}"
#             )
#
#             html = await fetch(http, list_url)
#             if not html:
#                 break
#
#             cars = parse_base_car_info(html)
#             if not cars:
#                 break
#
#             async def worker(car):
#                 async with sem:
#                     try:
#                         car_create = await scraper.scrape(car)
#                         if not car_create:
#                             return
#
#                         async with async_session_factory() as db:
#                             await save_car(db, car_create)
#                             await db.commit()
#
#
#                     except Exception as e:
#                         print(f"Error processing car {car.url}: {e}")
#
#             results = await asyncio.gather(
#                 *(worker(car) for car in cars),
#                 return_exceptions=True,
#             )
#
#             page += 1



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




# async def scrape_all_cars(
#     max_pages: int | None = None,
#     concurrent_requests: int = 5,
# ):
#
#
#     sem = asyncio.Semaphore(concurrent_requests)
#     timeout = aiohttp.ClientTimeout(total=30)
#
#     async with aiohttp.ClientSession(
#         timeout=timeout,
#         headers={"User-Agent": settings.app.user_agent},
#         cookies=settings.app.cookies,
#     ) as http, PhoneClient(settings.app.cookies) as phone_client:
#
#         scraper = CarDetailScraper(http, phone_client)
#
#         for page in range(max_pages):
#             list_url = (
#                 settings.app.start_url
#                 if page == 0
#                 else f"https://auto.ria.com/uk/search/?indexName=auto&page={page}"
#             )
#
#             print(f"📄 FETCHING PAGE {page + 1}: {list_url}")
#
#             html = await fetch(http, list_url)
#             if not html:
#                 break
#
#             cars = parse_base_car_info(html)
#             if not cars:
#                 break
#
#             async def worker(car):
#                 async with sem:
#                     car_create = await scraper.scrape(car)
#                     if not car_create:
#                         return
#
#                     # ✅ ВАЖНО: своя DB-сессия на каждый car
#                     async with async_session_factory() as db:
#                         await save_car(db, car_create)
#                         await db.commit()
#
#             await asyncio.gather(*(worker(car) for car in cars))
#
#     print("✅ SCRAPER FINISHED")

# async def scrape_all_cars(max_pages: int = 2, concurrent_requests: int = 5):
#     print("🔥 START SCRAPER")
#     sem = asyncio.Semaphore(concurrent_requests)
#     phone_client = PhoneClient(cookies=settings.app.cookies)
#
#     async def scrape_car_safe(car, session, db):
#         async with sem:
#             await scrape_car(car, session, db, phone_client)
#
#     async with aiohttp.ClientSession() as http:
#         async with async_session_factory() as db:
#             for page in range(max_pages):
#                 list_url = settings.app.start_url if page == 0 else f"https://auto.ria.com/uk/search/?indexName=auto&page={page}"
#                 print(f"📄 FETCHING PAGE {page + 1}: {list_url}")
#
#                 html = await fetch_list_page(http, list_url)
#                 if not html:
#                     break
#
#                 base_cars = parse_base_car_info(html)
#                 print(f"🔎 PAGE {page + 1} CARS FOUND: {len(base_cars)}")
#
#                 await asyncio.gather(*(scrape_car_safe(car, http, db) for car in base_cars))
#
#                 await db.commit()
#                 await asyncio.sleep(0.3)
#
#     print("✅ SCRAPER FINISHED")
