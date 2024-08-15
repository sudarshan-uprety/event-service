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


class ProductItem(BaseModel):
    product_id: str
    quantity: int


class OrderEventEmail(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    product: list[ProductItem]
    total_price: float
    vendor_name: str
