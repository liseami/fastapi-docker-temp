from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from app.models.table import SMSCodeRecord


class SMSCodeRecordCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_sms_code_record(
        self,
        phone_number: str,
        sms_code: int,
        expire_time: datetime,
        client_ip: str
    ) -> SMSCodeRecord:
        """创建短信验证码记录"""
        record = SMSCodeRecord(
            phone_number=phone_number,
            sms_code=sms_code,
            expire_time=expire_time,
            client_ip=client_ip
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def get_sms_code_record(self, record_id: int) -> Optional[SMSCodeRecord]:
        """根据ID获取短信验证码记录"""
        return self.session.get(SMSCodeRecord, record_id)

    def get_active_sms_code_records(
        self,
        phone_number: str,
        client_ip: str | None = None
    ) -> List[SMSCodeRecord]:
        """获取未过期的验证码记录"""
        query = select(SMSCodeRecord).where(
            SMSCodeRecord.phone_number == phone_number,
            SMSCodeRecord.expire_time > datetime.now()
        )

        if client_ip:
            query = query.where(SMSCodeRecord.client_ip == client_ip)

        return self.session.exec(query).all()

    def delete_expired_records(self) -> int:
        """删除所有过期的验证码记录，返回删除的记录数"""
        stmt = select(SMSCodeRecord).where(
            SMSCodeRecord.expire_time <= datetime.now())
        expired_records = self.session.exec(stmt).all()

        count = 0
        for record in expired_records:
            self.session.delete(record)
            count += 1

        self.session.commit()
        return count

    def delete_sms_code_record(self, record_id: int) -> bool:
        """删除指定的验证码记录"""
        record = self.get_sms_code_record(record_id)
        if not record:
            return False

        self.session.delete(record)
        self.session.commit()
        return True

    def verify_sms_code(
        self,
        phone_number: str,
        sms_code: int,
        client_ip: str | None = None
    ) -> bool:
        """验证短信验证码是否有效"""
        active_records = self.get_active_sms_code_records(
            phone_number, client_ip)

        for record in active_records:
            if record.sms_code == sms_code and not record.is_expired():
                return True

        return False
