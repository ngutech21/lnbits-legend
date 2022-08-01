import asyncio
from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer
from apscheduler.schedulers.asyncio import AsyncIOScheduler


db = Database("ext_scheduler")
apscheduler = AsyncIOScheduler()

scheduler_ext: APIRouter = APIRouter(prefix="/scheduler", tags=["scheduler"])


def scheduler_renderer():
    return template_renderer(["lnbits/extensions/scheduler/templates"])


from .views import *  # noqa
from .views_api import *  # noqa


def scheduler_start():
    loop = asyncio.get_event_loop()
    loop.create_task(create_apjobs(apscheduler))

    # apscheduler.add_job(tick,'interval', seconds=2)
    apscheduler.start()
