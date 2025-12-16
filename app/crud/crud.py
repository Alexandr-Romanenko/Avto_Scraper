from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.car import Car
from app.schemas.car import CarCreate


async def save_car(db: AsyncSession, car_in: dict | CarCreate):
    data = car_in if isinstance(car_in, dict) else car_in.model_dump()

    car_vin = data.get("car_vin")
    car_number = data.get("car_number")

    stmt = insert(Car).values(**data)

    # Если есть VIN + car_number, используем составной уникальный индекс
    if car_vin and car_number:
        stmt = stmt.on_conflict_do_nothing(index_elements=["car_vin", "car_number"])
    else:
        # Иначе fallback на уникальный URL
        stmt = stmt.on_conflict_do_nothing(index_elements=["url"])

    await db.execute(stmt)
    await db.commit()

# async def save_car(db: AsyncSession, car_in: CarCreate | dict):
#     data = car_in if isinstance(car_in, dict) else car_in.model_dump()
#
#     stmt = (
#         insert(Car)
#         .values(**data)
#         .on_conflict_do_update(
#             index_elements=["car_vin"],
#             set_={k: v for k, v in data.items() if k != "car_vin"}
#         )
#     )
#
#     await db.execute(stmt)


# async def save_car(db: AsyncSession, car_in: CarCreate | dict):
#     data = car_in if isinstance(car_in, dict) else car_in.model_dump()
#
#     stmt = (
#         insert(Car)
#         .values(**data)
#         .on_conflict_do_nothing(index_elements=["url"])
#     )
#
#     await db.execute(stmt)
