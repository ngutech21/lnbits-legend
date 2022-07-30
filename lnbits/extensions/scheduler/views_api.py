# views_api.py is for you API endpoints that could be hit by another service

# add your dependencies here

# import httpx
# (use httpx just like requests, except instead of response.ok there's only the
#  response.is_error that is its inverse)

from http import HTTPStatus
from typing import List

from fastapi import Query
from lnbits.extensions.scheduler.models import CreateJobConfig, JobConfig
from lnbits.extensions.scheduler.util import pay_jobconfig_invoice
from . import scheduler_ext
from fastapi.params import Depends
from loguru import logger
import traceback

logger.add("out.log", backtrace=True, diagnose=True)

from lnbits.decorators import (
    WalletTypeInfo,
    get_key_type
)


from .crud import create_jobconfig, delete_jobconfig, get_jobconfigs, update_jobconfig


@scheduler_ext.post("/api/v1/execute/")
async def api_jobconfig_execute(
    data: CreateJobConfig, wallet: WalletTypeInfo = Depends(get_key_type)
):
    jobConfig = JobConfig(id=123, wallet=data.wallet, lnurl=data.lnurl, timer_minute=data.timer_minute, description=data.description, amount=data.amount)
        
    await pay_jobconfig_invoice(jobConfig)
    return jobConfig.dict()


@scheduler_ext.post("/api/v1/jobconfigs")
async def api_jobconfig_create(
    data: CreateJobConfig, wallet: WalletTypeInfo = Depends(get_key_type)
):
    conf = await create_jobconfig(user=wallet.wallet.user, data=data)
    return conf.dict()


@scheduler_ext.put("/api/v1/jobconfigs/{jobconfig_id}")
async def api_jobconfig_update(
    data: CreateJobConfig, jobconfig_id: str= Query(None), wallet: WalletTypeInfo = Depends(get_key_type)
):
    conf = await update_jobconfig(user=wallet.wallet.user, jobconfig_id=jobconfig_id, data=data)
    return conf.dict()

@scheduler_ext.delete("/api/v1/jobconfigs/{jobconfig_id}")
async def api_jobconfig_update(
    jobconfig_id: str= Query(None), wallet: WalletTypeInfo = Depends(get_key_type)
):
    await delete_jobconfig(user=wallet.wallet.user, jobconfig_id=jobconfig_id)
    


@scheduler_ext.get("/api/v1/jobconfigs")
async def api_jobconfig_retrieve(wallet: WalletTypeInfo = Depends(get_key_type)):
    logger.info("jobconfig_retrieve")
    print("jobconfig_retrieve")
    try:
        return [
            {**jobconfig.dict()}
            for jobconfig in await get_jobconfigs(wallet.wallet.user)
        ]
    except:
        print("error")
        traceback.print_exc()
        logger.error("error calling api_jobconfig_retrieve")
        return ""


@scheduler_ext.get("/api/v1/tools")
async def api_scheduler():
    """Try to add descriptions for others."""
    tools = [
        {
            "name": "fastAPI",
            "url": "https://fastapi.tiangolo.com/",
            "language": "Python",
        },
        {
            "name": "Vue.js",
            "url": "https://vuejs.org/",
            "language": "JavaScript",
        },
        {
            "name": "Quasar Framework",
            "url": "https://quasar.dev/",
            "language": "JavaScript",
        },
    ]

    return tools
