from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from app.core.security import get_password_hash
from app.models.table import User
from app.models.base_models.UserBase import UserCreate
from app.tool.random import RandomGenerator


class UserCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: str) -> User | None:
        """根据UUID获取用户"""
        return self.session.get(User, user_id)

    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        """根据手机号获取用户"""
        return self.session.exec(
            select(User)
            .where(User.phone_number == phone_number, User.is_deleted == False)
        ).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.session.exec(
            select(User)
            .where(User.username == username, User.is_deleted == False)
        ).first()

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """获取用户列表"""
        statement = select(User).where(User.is_deleted ==
                                       False).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create_super_user(self, phone_number: str, username: str, password: str) -> User:
        """创建新用户"""
        # 验证数据并哈希密码
        new = UserCreate(
            phone_number=phone_number,
            username=username,
            password=password,
            is_active=True,
            is_superuser=True
        )
        new_user = User.model_validate(
            new,
            update={"hashed_password": get_password_hash(new.password)}
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def create_user(self, phone_number: str) -> User:
        """创建新用户"""
        # 验证数据并哈希密码
        new = UserCreate(
            phone_number=phone_number,
            username=RandomGenerator().generate_username(prefix="Fastapi模版App"),
            password=RandomGenerator().generate_password(length=12),
            is_active=True,
            is_superuser=False
        )
        new_user = User.model_validate(
            new,
            update={"hashed_password": get_password_hash(new.password)}
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def update_user(
        self,
        user_id: UUID,
        update_data: dict
    ) -> Optional[User]:
        """更新用户信息

        Args:
            user_id (UUID): 需要更新的用户ID
            update_data (dict): 包含要更新的字段和值的字典
                例如: {"username": "新用户名"}

        Returns:
            Optional[User]: 更新成功返回更新后的用户对象,用户不存在或已删除返回None

        说明:
            - 只允许更新username字段
            - 其他字段的更新请求将被忽略
        """
        # 获取用户并检查是否存在或已删除
        user = self.get_user(user_id)
        if not user or user.is_deleted:
            return None

        # 将update_data中字段为空的值剔除
        update_data = {k: v for k, v in update_data.items() if v is not None}

        # 只更新username字段
        if "username" in update_data:
            user.username = update_data["username"]

        # 保存更新到数据库
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def delete_user(self, user_id: UUID) -> bool:
        """软删除用户"""
        user = self.get_user(user_id)
        if not user or user.is_deleted:
            return False

        user.is_deleted = True
        self.session.add(user)
        self.session.commit()
        return True
