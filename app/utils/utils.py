import re


def normalize_odometer(text: str | None) -> int | None:
    if not text:
        return None

    text = text.lower().replace("\xa0", " ").strip()

    match = re.search(r"(\d+(?:[.,]\d+)?)", text)
    if not match:
        return None

    value = float(match.group(1).replace(",", "."))

    if "тис" in text:
        value *= 1_000
    elif "млн" in text:
        value *= 1_000_000

    return int(value)


def extract_ids_from_html(html: str) -> tuple[str | None, str | None]:
    user_id = None
    phone_id = None

    user_match = re.search(r'"userId","(\d+)"', html)
    phone_match = re.search(r'"phoneId","(\d+)"', html)

    if user_match:
        user_id = user_match.group(1)

    if phone_match:
        phone_id = phone_match.group(1)

    return user_id, phone_id


AUTO_ID_RE = re.compile(r"_([0-9]+)\.html")

def extract_auto_id_from_url(url: str) -> int:
    match = AUTO_ID_RE.search(url)
    if not match:
        raise ValueError(f"Cannot extract auto_id from url: {url}")
    return int(match.group(1))