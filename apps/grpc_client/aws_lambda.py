from apps.lambda_events.proto import aws_lambda_pb2_grpc, aws_lambda_pb2
from utils import variables
from apps.lambda_events.schema import Product, InventoryProducer
from apps.lambda_events.call_lambda import call_lambda

class LambdaService(aws_lambda_pb2_grpc.InventoryServiceServicer):
    async def ProcessEvent(self, request: InventoryProducer, context):
        # Convert gRPC request to dict
        body_dict = {
            "trace_id": request.trace_id,
            "event_name": request.event_name,
            "products": self.convert_products_to_dict(request.products)
        }
        
        data = await call_lambda(data=body_dict)

        return aws_lambda_pb2.ProcessEventResponse(
            message=data['message'],
            success=data['success']
        )

    def convert_products_to_dict(self, products):
        return [{
            "product_id": product.product_id,
            "quantity": product.quantity,
            "size": product.size,
            "color": product.color
        } for product in products]