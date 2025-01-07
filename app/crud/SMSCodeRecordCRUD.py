from datetime import datetime, timedelta
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
    ) -> SMSCodeRecord:
        """创建短信验证码记录"""
        # 设置过期时间为5分钟后
        expire_time = datetime.now() + timedelta(minutes=1)
        record = SMSCodeRecord(
            phone_number=phone_number,
            sms_code=sms_code,
            expire_time=expire_time,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def get_sms_code_record(self, record_id: int) -> Optional[SMSCodeRecord]:
        """根据ID获取短信验证码记录"""
        return self.session.get(SMSCodeRecord, record_id)

    def get_latest_sms_code_record(self, phone_number: str) -> Optional[SMSCodeRecord]:
        """获取指定手机号最新的验证码记录"""
        return self.session.exec(
            select(SMSCodeRecord)
            .where(SMSCodeRecord.phone_number == phone_number)
            .order_by(SMSCodeRecord.created_at.desc())
        ).first()

    def get_active_sms_code_records(
        self,
        phone_number: str,
    ) -> List[SMSCodeRecord]:
        """获取未过期的验证码记录"""
        query = select(SMSCodeRecord).where(
            SMSCodeRecord.phone_number == phone_number,
            SMSCodeRecord.expire_time > datetime.now()
        )
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
    ) -> bool:
        """验证短信验证码是否有效"""
        active_records = self.get_active_sms_code_records(phone_number)

        for record in active_records:
            if record.sms_code == sms_code and not record.is_expired():
                return True

        return False
