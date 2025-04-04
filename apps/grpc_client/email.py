from apps.email_events.proto import email_pb2, email_pb2_grpc
from utils import variables
from apps.email_events.schema import RegisterEmail, OrderEventEmail
from apps.email_events.send_mail import register_mail, forget_password_mail, order_confirmation_mail

class EmailService(email_pb2_grpc.EmailServiceServicer):
    async def RegisterSendEmail(self, request, context):
        # Convert gRPC request to dict (you can use `.dict()` if using Pydantic)
        body_dict = {
            "trace_id": request.trace_id,
            "to": request.to,
            "event_name": request.event_name,
            "otp": request.otp,
            "full_name": request.full_name
        }
        # Handle event based on name
        if request.event_name == variables.REGISTER_EMAIL:
            data = RegisterEmail(**body_dict)
        else:
            return email_pb2.EmailResponse(success=False, message="Unknown event")

        await register_mail(to=data.to, name=data.full_name, otp=data.otp)
        
        return email_pb2.EmailResponse(
            message="Registration email sent successfully",
            success=True
        )

    async def ForgetPasswordSendEmail(self, request, context):
        # Convert gRPC request to dict (you can use `.dict()` if using Pydantic)
        body_dict = {
            "trace_id": request.trace_id,
            "to": request.to,
            "event_name": request.event_name,
            "otp": request.otp,
            "full_name": request.full_name
        }
        # Handle event based on name
        if request.event_name == variables.FORGET_PASSWORD_EMAIL:
            data = RegisterEmail(**body_dict)
        else:
            return email_pb2.EmailResponse(success=False, message="Unknown event")

        await forget_password_mail(to=data.to, name=data.full_name, otp=data.otp)
        
        return email_pb2.EmailResponse(
            message="Forget password email sent successfully",
            success=True
        )


    async def OrderConfirmationSendEmail(self, request, context):
        # Handling Order Confirmation Email event
        products_list = []
        for product in request.products:
            products_list.append({
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price, 
                "total": product.total
            })
        body_dict = {
            "trace_id": request.trace_id,
            "event_name": request.event_name,
            "to": request.to,
            "products": products_list,
            "total_price": request.total_price,
            "full_name": request.full_name,
            "order_id": request.order_id,
            "customer_phone": request.customer_phone,
            "delivery_address": request.delivery_address,
            "payment_id": request.payment_id,
            "payment_amount": request.payment_amount,
            "payment_method": request.payment_method,
            "payment_status": request.payment_status,
            "order_date": request.order_date
        }


        if request.event_name == variables.ORDER_CONFIRMATION_EMAIL:
            data = OrderEventEmail(**body_dict)
        else:
            return email_pb2.EmailResponse(success=False, message="Unknown event")

        # Call the function that sends the order confirmation email
        await order_confirmation_mail(data)

        return email_pb2.EmailResponse(
            message="Order confirmation email sent successfully",
            success=True
        )
