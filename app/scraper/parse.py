import re
from bs4 import BeautifulSoup
from app.schemas.car import CarBase, CarDetail


def parse_base_car_info(html: str) -> list[CarBase]:
    """Парсинг базовой информации о машинах со страницы списка."""
    soup = BeautifulSoup(html, "lxml")
    cars: list[CarBase] = []

    cards = soup.select("a.link.product-card.horizontal")
    for card in cards:
        href = card.get("href")
        url = href if href.startswith("http") else "https://auto.ria.com" + href

        title_tag = card.select_one(
            "div.product-card-content div.structure-row.mb-8 div.grow-1.basis-0 "
            "div.common-text.size-16-20.titleS.fw-bold.mb-4"
        )
        title = title_tag.get_text(strip=True) if title_tag else None

        price_tag = card.select_one("span.common-text.titleM.c-green")
        price = None
        if price_tag:
            raw = re.sub(r"[^\d.]", "", price_tag.get_text().replace("\xa0", "").replace(" ", ""))
            price = float(raw) if raw else None

        odometer_tag = card.select_one(".ellipsis-1.body")
        odometer = odometer_tag.get_text(strip=True) if odometer_tag else None

        cars.append(CarBase(url=url, title=title, price_usd=price, odometer=odometer))

    return cars


def parse_detail_car_info(html: str, car: CarBase) -> CarDetail:
    """Парсинг детальной информации о машине (без телефона)."""
    soup = BeautifulSoup(html, "lxml")

    def get_text(selector: str) -> str | None:
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else None

    username = get_text("div#sellerInfoUserName span")
    car_vin = get_text("div#badgesVinGrid div.badge-template span.common-text.ws-pre-wrap.badge")
    car_number = get_text("div.car-number.ua span")

    # IDs для запроса телефона
    # user_id, phone_id = extract_ids_from_html(html)
    # auto_id = extract_auto_id_from_url(car.url)

    # Images
    images: list[str] = []
    carousel = soup.select_one("div.carousel__viewport")
    if carousel:
        for img in carousel.select("picture img"):
            url = img.get("data-src") or img.get("src")
            if url and url.endswith(".webp"):
                url = url.rsplit(".", 1)[0] + ".jpg"
            if url:
                images.append(url)

    if not images:
        picture_tag = soup.select_one("span.picture picture img")
        if picture_tag:
            url = picture_tag.get("data-src") or picture_tag.get("src")
            if url and url.endswith(".webp"):
                url = url.rsplit(".", 1)[0] + ".jpg"
            if url:
                images.append(url)

    image_url = images[0] if images else None
    images_count = len(images)

    return CarDetail(
        username=username,
        phone_number=None,
        car_vin=car_vin,
        car_number=car_number,
        image_url=image_url,
        images_count=images_count,
    )
