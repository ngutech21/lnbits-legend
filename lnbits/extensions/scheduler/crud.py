from typing import List

from loguru import logger

from lnbits.helpers import urlsafe_short_hash
from lnbits.extensions.scheduler import db
from lnbits.extensions.scheduler.models import CreateJobConfig, JobConfig


async def get_jobconfigs(user: str) -> List[JobConfig]:
    logger.debug(f"user {user}")
    rows = await db.fetchall(
        """SELECT * FROM scheduler.job_config WHERE "user_name" = ?""", (user,)
    )
    return [JobConfig.from_row(row) for row in rows]


# FIXME merge with get_jobconfigs()
async def get_all_jobconfigs() -> List[JobConfig]:
    rows = await db.fetchall("""SELECT * FROM scheduler.job_config """)
    return [JobConfig.from_row(row) for row in rows]


async def get_jobconfig(user: str, id: str) -> JobConfig:
    logger.debug(f"user {user}")
    rows = await db.fetchall(
        """SELECT * FROM scheduler.job_config WHERE "user_name" = ? and id=? """,
        (user, id),
    )
    return rows[0]


async def create_jobconfig(user: str, data: CreateJobConfig) -> JobConfig:
    logger.debug(f"create_jobconfig user {user}")
    jobconfig_id = urlsafe_short_hash()
    rows = await db.execute(
        """INSERT INTO scheduler.job_config(
	       id, user_name, wallet, lnurl, description, timer_minute, amount)
	       VALUES (?, ?, ?, ?, ?, ?, ?);""",
        (
            jobconfig_id,
            user,
            data.wallet,
            data.lnurl,
            data.description,
            data.timer_minute,
            data.amount,
        ),
    )
    return await get_jobconfig_allusers(job_config_id=jobconfig_id)


async def update_jobconfig_scheduler_job_id(
    user: str, jobconfig_id: str, scheduler_job_id: str
) -> JobConfig:
    logger.debug(f"create_jobconfig user {user} jobid {scheduler_job_id}")
    rows = await db.execute(
        """UPDATE scheduler.job_config
	       SET scheduler_job_id = ?
	       WHERE id = ?;""",
        (
            scheduler_job_id,
            jobconfig_id,
        ),
    )
    return await get_jobconfig_allusers(job_config_id=jobconfig_id)


async def update_jobconfig(
    user: str, jobconfig_id: str, data: CreateJobConfig
) -> JobConfig:
    logger.debug(f"create_jobconfig user {user} data {data}")
    rows = await db.execute(
        """UPDATE scheduler.job_config
	       SET wallet=?, lnurl=?, description=?, timer_minute=?, amount = ?
	       WHERE id=?;""",
        (
            data.wallet,
            data.lnurl,
            data.description,
            data.timer_minute,
            data.amount,
            jobconfig_id,
        ),
    )
    return await get_jobconfig_allusers(job_config_id=jobconfig_id)


async def delete_jobconfig(user: str, jobconfig_id: str) -> None:
    logger.debug(f"delete_jobconfig user {user}")
    return await db.execute(
        """DELETE FROM scheduler.job_config
	       WHERE id=?;""",
        (jobconfig_id),
    )


async def get_jobconfig_allusers(job_config_id: str) -> JobConfig:
    rows = await db.fetchall(
        """SELECT * FROM scheduler.job_config WHERE id = ?""", (job_config_id)
    )
    if len(rows) > 0:
        return JobConfig.from_row(rows[0])
    return
