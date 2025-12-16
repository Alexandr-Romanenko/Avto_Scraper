from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, Index

from app.models.base import Base


class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    title: Mapped[str | None] = mapped_column(nullable=True)
    price_usd: Mapped[float | None] = mapped_column(nullable=True)
    odometer: Mapped[int | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    phone_number: Mapped[str | None] = mapped_column(nullable=True)
    image_url: Mapped[str | None] = mapped_column(nullable=True)
    images_count: Mapped[int | None] = mapped_column(nullable=True)
    car_number: Mapped[str | None] = mapped_column(nullable=True)
    car_vin: Mapped[str | None] = mapped_column(nullable=True)
    datetime_found: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    __table_args__ = (
        Index(
            "uq_car_vin_number",
            "car_vin",
            "car_number",
            unique=True
        ),
    )


