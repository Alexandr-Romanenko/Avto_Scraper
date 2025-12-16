import aiohttp

from app.scraper.fetch import fetch
from app.scraper.fetch_phone import PhoneClient
from app.scraper.parse import parse_detail_car_info
from app.schemas.car import CarBase, CarCreate
from app.utils.utils import extract_ids_from_html, extract_auto_id_from_url


class CarDetailScraper:
    def __init__(
        self,
        http: aiohttp.ClientSession,
        phone_client: PhoneClient,
    ):
        self.http = http
        self.phone_client = phone_client

    async def scrape(self, car: CarBase) -> CarCreate | None:
        html = await fetch(self.http, car.url)
        if not html:
            return None

        detail = parse_detail_car_info(html, car)

        phone_number = await self._get_phone(html, car.url)

        return CarCreate(
            **car.model_dump(),
            **detail.model_dump(exclude={"phone_number"}),
            phone_number=phone_number,
        )

    async def _get_phone(self, html: str, url: str) -> str | None:
        user_id, phone_id = extract_ids_from_html(html)
        auto_id = extract_auto_id_from_url(url)

        if not (user_id and phone_id and auto_id):
            return None

        return await self.phone_client.get_phone(
            auto_id=auto_id,
            user_id=user_id,
            phone_id=phone_id,
        )



# async def scrape_car(
#     car: CarBase,
#     http: aiohttp.ClientSession,
#     db: AsyncSession,
#     phone_client: PhoneClient,
# ):
#     html = await fetch(http, car.url)
#     if not html:
#         return
#
#     detail = parse_detail_car_info(html, car)
#
#     if detail.user_id and detail.phone_id:
#         detail.phone_number = await phone_client.get_phone(
#             http,
#             detail.auto_id,
#             detail.user_id,
#             detail.phone_id,
#         )
#
#     car_create = CarCreate(**detail.model_dump(exclude={"auto_id", "user_id", "phone_id"}))
#
#     await save_car(db, car_create)


# async def scrape_car(car: CarBase, http: aiohttp.ClientSession, db: AsyncSession):
#     """Скрейпинг деталей одной машины и сохранение в БД."""
#     print("📄 fetch car:", car.url)
#     html = await fetch(http, car.url)
#     if not html:
#         return
#     car_full = parse_detail_car_info(html, car)
#     await save_car(db, car_full)
