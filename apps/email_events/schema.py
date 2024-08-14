from pydantic import BaseModel, EmailStr


class RegisterMail(BaseModel):
    otp: str
    to: EmailStr
    name: str


class ForgetPassword(BaseModel):
    otp: str
    name: str
    to: EmailStr
