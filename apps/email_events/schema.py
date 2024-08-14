from pydantic import BaseModel, EmailStr


# class RegisterMail(BaseModel):
#     otp: str
#     to: EmailStr
#     name: str
#
#
# class ForgetPassword(BaseModel):
#     otp: str
#     name: str
#     to: EmailStr


class RegisterEmail(BaseModel):
    event_name: str
    trace_id: str
    to: EmailStr
    otp: str
    full_name: str


class ForgetPasswordEmail(BaseModel):
    event_name: str
    trace_id: str
    to: EmailStr
    otp: str
    full_name: str
