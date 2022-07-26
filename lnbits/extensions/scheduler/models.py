from fastapi import Query
from pydantic import BaseModel
from sqlite3 import Row


class JobConfig(BaseModel):
    id: str
    wallet: str
    lnurl: str
    timer_minute: int
    description: str

    @classmethod
    def from_row(cls, row: Row) -> "JobConfig":
        return cls(**dict(row))


class CreateJobConfig(BaseModel):
    lnurl: str = Query(...)
    wallet: str = Query(...)
    timer_minute: int = Query(...)
    description: str = Query(...)
