

from sqlmodel import SQLModel, Field
from datetime import datetime
import time


class SMSCodeRecordBase(SQLModel):
    create_time: datetime = Field(default_factory=datetime.now)
    expire_time: datetime = Field(...)
    phone_number: str = Field(default="")
    sms_code: int = Field(default=0)
    client_ip: str = Field(default="")

    def is_expired(self) -> bool:
        return datetime.now > self.expire_time

    def sec_to_open(self) -> int:
        time_diff = self.expire_time - datetime.now
        return max(0, int(time_diff))
