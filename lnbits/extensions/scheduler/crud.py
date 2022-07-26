from typing import List

from loguru import logger

from lnbits.extensions.satspay.crud import get_charge
from lnbits.helpers import urlsafe_short_hash
from . import db
from .models import CreateJobConfig, JobConfig


async def get_jobconfigs(user: str) -> List[JobConfig]:
    logger.debug(f"user {user}")
    rows = await db.fetchall(
        """SELECT * FROM scheduler.job_config WHERE "user_name" = ?""", (user,)
    )
    return [JobConfig.from_row(row) for row in rows]


async def create_jobconfig(user: str, data: CreateJobConfig) -> JobConfig:
    logger.debug(f"create_jobconfig user {user}")
    jobconfig_id = urlsafe_short_hash()
    rows = await db.execute(
        """INSERT INTO scheduler.job_config(
	       id, user_name, wallet, lnurl, description, timer_minute)
	       VALUES (?, ?, ?, ?, ?, ?);""",
        (jobconfig_id, user, data.wallet, data.lnurl, data.description, data.timer_minute),
    )
    return await get_jobconfig(jobconfig_id)

async def update_jobconfig(user: str, jobconfig_id: str,  data: CreateJobConfig) -> JobConfig:
    logger.debug(f"create_jobconfig user {user} data {data}")
    rows = await db.execute(
        """UPDATE scheduler.job_config
	       SET wallet=?, lnurl=?, description=?, timer_minute=?
	       WHERE id=?;""",
        (data.wallet, data.lnurl, data.description, data.timer_minute, jobconfig_id),
    )
    return await get_jobconfig(jobconfig_id)


async def get_jobconfig(job_config_id: str) -> JobConfig:
    rows = await db.fetchall(
        """SELECT * FROM scheduler.job_config WHERE id = ?""", (job_config_id)
    )
    if len(rows) > 0:
        return JobConfig.from_row(rows[0]) 
    return 