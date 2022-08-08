from typing import Optional
from fastapi import Query
from loguru import logger
from pydantic import BaseModel
from sqlite3 import Row


class JobConfig(BaseModel):
    id: str
    wallet: str
    lnurl: str
    timer_minute: int
    description: str
    amount: int
    scheduler_job_id: Optional[str]

    @classmethod
    def from_row(cls, row: Row) -> "JobConfig":
        logger.debug(f"from row {row}")
        return cls(**dict(row))


class CreateJobConfig(BaseModel):
    lnurl: str = Query(...)
    wallet: str = Query(...)
    timer_minute: int = Query(...)
    description: str = Query(...)
    amount: int = Query(...)
