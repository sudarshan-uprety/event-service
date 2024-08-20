from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


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

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class PaymentInfo(BaseModel):
    payment_id: str
    payment_amount: float
    payment_type: str


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
    name: str
    quantity: int
    price: float
    total: float


class OrderEventEmail(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    products: List[ProductItem]
    total_price: float
    order_id: str
    full_name: str
    customer_phone: str
    delivery_address: str
    payment_id: str
    payment_amount: float
    payment_method: str
    payment_status: str
    order_date: datetime
