# from sqlmodel import Session
# from sqlmodel import Session, select
# from app.core.security import get_password_hash, verify_password
# from app.models.table import User


# # 通过手机号，获取用户
# def get_user_by_phone(*, session: Session, phone_number: str) -> User | None:
#     statement = select(User).where(User.phone_number == phone_number)
#     session_user = session.exec(statement).first()
#     return session_user


# def authenticate(*, session: Session, phone_number: str, password: str) -> User | None:
#     db_user = get_user_by_phone(session=session, phone_number=phone_number)
#     if not db_user:
#         return None
#     if not verify_password(password, db_user.hashed_password):
#         return None
#     return db_user
