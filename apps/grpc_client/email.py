from apps.email_events.proto import email_pb2, email_pb2_grpc
from utils import variables
from apps.email_events.schema import RegisterEmail, OrderEventEmail
from apps.email_events.send_mail import register_mail, forget_password_mail, order_confirmation_mail

class EmailService(email_pb2_grpc.EmailServiceServicer):
    async def SendEmail(self, request, context):
        # Convert gRPC request to dict (you can use `.dict()` if using Pydantic)
        body_dict = {
            "trace_id": request.trace_id,
            "to": request.to,
            "event_name": request.event_name,
            "otp": request.otp,
            "full_name": request.full_name
        }
        # Handle event based on name
        if request.event_name in [variables.REGISTER_EMAIL, variables.FORGET_PASSWORD_EMAIL]:
            data = RegisterEmail(**body_dict)
        elif request.event_name == variables.ORDER_CONFIRMATION_EMAIL:
            data = OrderEventEmail(**body_dict)
        else:
            return email_pb2.EmailResponse(success=False, message="Unknown event")

        # Route to appropriate email handler
        if data.event_name == variables.REGISTER_EMAIL:
            await register_mail(to=data.to, name=data.full_name, otp=data.otp)
        elif data.event_name == variables.FORGET_PASSWORD_EMAIL:
            await forget_password_mail(to=data.to, name=data.full_name, otp=data.otp)
        elif data.event_name == variables.ORDER_CONFIRMATION_EMAIL:
            await order_confirmation_mail(data)
        
        return email_pb2.EmailResponse(
            message="Email sent successfully",
            success=True
        )