from pydantic import BaseModel

class ScheduledPayment(BaseModel):
    id: str
    wallet: str
    lnurl: str
