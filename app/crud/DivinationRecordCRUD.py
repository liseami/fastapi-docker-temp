from typing import List, Optional
from sqlmodel import Session, select
from app.models.table import DivinationRecord


class DivinationRecordCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_all_records(self, user_id: str) -> List[DivinationRecord]:
        """获取指定用户的所有占卜记录"""
        stmt = select(DivinationRecord).where(
            DivinationRecord.user_id == user_id,
            DivinationRecord.is_deleted == False
        )
        return self.session.exec(stmt).all()

    def create_record(
        self,
        title: str,
        question: str,
        current_gua: str,
        change_gua: str,
        ai_answer: str,
        user_id: str
    ) -> DivinationRecord:
        """创建新的占卜记录"""
        new_record = DivinationRecord(
            title=title,
            question=question,
            current_gua=current_gua,
            change_gua=change_gua,
            ai_answer=ai_answer,
            user_id=user_id
        )
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        return new_record

    def get_record(self, record_id: str, user_id: str) -> Optional[DivinationRecord]:
        """根据ID获取占卜记录，并验证所有权"""
        record = self.session.get(DivinationRecord, record_id)
        print(f"获取记录结果: {record}")
        if record and record.user_id == user_id:
            return record
        return None

    def update_record(
        self,
        record_id: str,
        user_id: str,
        title: Optional[str] = None,
        question: Optional[str] = None,
        current_gua: Optional[str] = None,
        change_gua: Optional[str] = None,
        ai_answer: Optional[str] = None
    ) -> Optional[DivinationRecord]:
        """更新占卜记录，需验证所有权"""
        print("开始更新占卜记录")
        print(f"记录ID: {record_id}, 用户ID: {user_id}")

        # 获取并验证记录所有权
        record = self.get_record(record_id, user_id)
        print(f"获取记录结果: {record}")
        if not record:
            print("记录不存在或无权限访问")
            return None

        # 更新标题字段
        if title is not None:
            print(f"更新标题: {title}")
            record.title = title
        # 更新问题字段
        if question is not None:
            print(f"更新问题: {question}")
            record.question = question
        # 更新当前卦象字段
        if current_gua is not None:
            print(f"更新当前卦象: {current_gua}")
            record.current_gua = current_gua
        # 更新变卦字段
        if change_gua is not None:
            print(f"更新变卦: {change_gua}")
            record.change_gua = change_gua
        # 更新AI回答字段
        if ai_answer is not None:
            print(f"更新AI回答: {ai_answer[:100]}...")  # 只打印前100个字符
            record.ai_answer = ai_answer

        # 将更新后的记录添加到会话
        print("添加更新记录到会话")
        self.session.add(record)
        # 提交更改到数据库
        print("提交更改到数据库")
        self.session.commit()
        # 刷新记录以获取最新数据
        print("刷新记录数据")
        self.session.refresh(record)
        print("记录更新完成")
        return record

    def delete_record(self, record_id: str, user_id: str) -> bool:
        """软删除占卜记录，需验证所有权"""
        record = self.get_record(record_id, user_id)
        if not record:
            return False
        record.is_deleted = True
        self.session.add(record)
        self.session.commit()
        return True

    def get_record_by_title(self, title: str, user_id: str) -> Optional[DivinationRecord]:
        """根据标题查找占卜记录"""
        stmt = select(DivinationRecord).where(
            DivinationRecord.title == title,
            DivinationRecord.user_id == user_id,
            DivinationRecord.is_deleted == False
        )
        return self.session.exec(stmt).first()
