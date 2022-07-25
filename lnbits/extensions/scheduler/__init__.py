from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer

db = Database("ext_scheduler")

scheduler_ext: APIRouter = APIRouter(prefix="/scheduler", tags=["scheduler"])


def scheduler_renderer():
    return template_renderer(["lnbits/extensions/scheduler/templates"])


from .views import *  # noqa
from .views_api import *  # noqa
