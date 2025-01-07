

from sqlmodel import SQLModel, Field
from datetime import datetime
import time
from .Base import TableBase


class SMSCodeRecordBase(TableBase):
    # 验证码过期时间,必填字段
    expire_time: datetime = Field(
        ...,
        description="验证码的过期时间,UTC时间"
    )

    # 接收验证码的手机号
    phone_number: str = Field(
        default="",
        description="接收验证码的手机号码"
    )

    # 验证码数字
    sms_code: int = Field(
        default=0,
        description="短信验证码内容,整型存储"
    )

    def is_expired(self) -> bool:
        """
        检查验证码是否已过期

        Returns:
            bool: True表示已过期,False表示未过期
        """
        return datetime.now() > self.expire_time

    def sec_to_open(self) -> int:
        """
        计算验证码的剩余有效时间(秒)

        Returns:
            int: 剩余有效秒数,已过期返回0
        """
        time_diff = self.expire_time - datetime.now
        return max(0, int(time_diff))
