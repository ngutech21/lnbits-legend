import asyncio
from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from lnbits.settings import LNBITS_DATABASE_URL


db = Database("ext_scheduler")
apscheduler = AsyncIOScheduler()

scheduler_ext: APIRouter = APIRouter(prefix="/scheduler", tags=["scheduler"])


def scheduler_renderer():
    return template_renderer(["lnbits/extensions/scheduler/templates"])


from lnbits.extensions.scheduler.views import *  # noqa
from lnbits.extensions.scheduler.views_api import *  # noqa


def scheduler_start():
    apscheduler.add_jobstore(
        SQLAlchemyJobStore(url=LNBITS_DATABASE_URL, tableschema="scheduler")
    )
    loop = asyncio.get_event_loop()
    loop.create_task(create_apjobs())
    apscheduler.start()
