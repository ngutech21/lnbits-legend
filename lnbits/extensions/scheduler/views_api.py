# views_api.py is for you API endpoints that could be hit by another service

# add your dependencies here

# import httpx
# (use httpx just like requests, except instead of response.ok there's only the
#  response.is_error that is its inverse)


from fastapi import Query
from lnbits.extensions.scheduler.models import CreateJobConfig, JobConfig
from lnbits.extensions.scheduler.util import pay_jobconfig_invoice
from lnbits.extensions.scheduler import scheduler_ext, apscheduler
from fastapi.params import Depends
from loguru import logger
import traceback
from lnbits.decorators import WalletTypeInfo, get_key_type
from lnbits.extensions.scheduler.crud import (
    create_jobconfig,
    delete_jobconfig,
    get_all_jobconfigs,
    get_jobconfig,
    get_jobconfigs,
    update_jobconfig,
    update_jobconfig_scheduler_job_id,
)


def apscheduler_add_job(jobconfig: JobConfig) -> str:
    job = apscheduler.add_job(
        func=pay_jobconfig_invoice,
        trigger="interval",
        args=[jobconfig],
        seconds=jobconfig.timer_minute,  # FIXME  use seconds for testing purpose
    )
    jobconfig.scheduler_job_id = job.id
    return job.id


def apscheduler_update_job(jobconfig: JobConfig):
    logger.debug(f">>>apscheduler_update_job call")
    apscheduler.remove_job(job_id=jobconfig.scheduler_job_id)
    apscheduler_add_job(jobconfig=jobconfig)


def apscheduler_delete_job(jobconfigId: str):
    apscheduler.remove_job(jobconfigId)


async def create_apjobs():
    for j in await get_all_jobconfigs():
        print(f"create apjob {j}")
        apscheduler_add_job(j)


# FIXME remove execute API
@scheduler_ext.post("/api/v1/execute/")
async def api_jobconfig_execute(
    data: CreateJobConfig, wallet: WalletTypeInfo = Depends(get_key_type)
):
    jobConfig = JobConfig(
        id=123,  # FIXME
        wallet=data.wallet,
        lnurl=data.lnurl,
        timer_minute=data.timer_minute,
        description=data.description,
        amount=data.amount,
    )

    await pay_jobconfig_invoice(jobConfig)
    return jobConfig.dict()


@scheduler_ext.post("/api/v1/jobconfigs")
async def api_jobconfig_create(
    data: CreateJobConfig, wallet: WalletTypeInfo = Depends(get_key_type)
):
    conf = await create_jobconfig(user=wallet.wallet.user, data=data)
    scheduler_job_id = apscheduler_add_job(conf)
    logger.debug(f"create {conf} {scheduler_job_id}")
    await update_jobconfig_scheduler_job_id(
        user=wallet.wallet.user, jobconfig_id=conf.id, scheduler_job_id=scheduler_job_id
    )
    return conf.dict()


@scheduler_ext.put("/api/v1/jobconfigs/{jobconfig_id}")
async def api_jobconfig_update(
    data: CreateJobConfig,
    jobconfig_id: str = Query(None),
    wallet: WalletTypeInfo = Depends(get_key_type),
):
    conf = await update_jobconfig(
        user=wallet.wallet.user, jobconfig_id=jobconfig_id, data=data
    )
    apscheduler_update_job(conf)
    await update_jobconfig_scheduler_job_id(
        user=wallet.wallet.user,
        jobconfig_id=conf.id,
        scheduler_job_id=conf.scheduler_job_id,
    )
    return conf.dict()


@scheduler_ext.delete("/api/v1/jobconfigs/{jobconfig_id}")
async def api_jobconfig_update(
    jobconfig_id: str = Query(None), wallet: WalletTypeInfo = Depends(get_key_type)
):
    job = await get_jobconfig(jobconfig_id)
    apscheduler_delete_job(job.scheduler_job_id)  # FIXME error handling
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
