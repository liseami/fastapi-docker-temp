from sqlmodel import SQLModel


class PhoneNumberIn(SQLModel):
    phone_number: str
