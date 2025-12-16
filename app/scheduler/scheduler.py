from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.scheduler.jobs import scrape_job, dump_db_job
from app.config.settings import settings


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

    scheduler.add_job(
        scrape_job,
        CronTrigger(
            hour=settings.app.schedule_hour,
            minute=settings.app.schedule_minute,
        ),
        name="daily_scrape",
        replace_existing=True,
    )

    scheduler.add_job(
        dump_db_job,
        CronTrigger(
            hour=settings.app.schedule_hour,
            minute=settings.app.schedule_minute,
        ),
        name="daily_db_dump",
        replace_existing=True,
    )

    return scheduler
