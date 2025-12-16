from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, Field
from app.utils.utils import normalize_odometer


class FromAttributesMixin:
    class Config:
        from_attributes = True


class CarBase(FromAttributesMixin, BaseModel):
    url: str
    title: str | None
    price_usd: float | None = None
    odometer: int | None = None

    @field_validator("odometer", mode="before")
    @classmethod
    def normalize_odometer_field(cls, v):
        if v is None:
            return None
        if isinstance(v, int):
            return v
        return normalize_odometer(str(v))


class CarDetail(FromAttributesMixin, BaseModel):
    username: str | None
    phone_number: str | None = None
    image_url: str | None = None
    images_count: int | None = None
    car_number: str | None = None
    car_vin: str | None = None


class CarCreate(CarBase, CarDetail):
    datetime_found: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
