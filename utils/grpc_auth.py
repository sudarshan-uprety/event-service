import grpc

from apps.email_events.proto import email_pb2
from utils import variables

class APIKeyInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        api_key = metadata.get('x-api-key')

        if not api_key or api_key != variables.GRPC_API_KEY:
            def deny_request(request, context):
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Invalid API key")
                return None  # or raise grpc.RpcError, but this works cleaner here

            return grpc.unary_unary_rpc_method_handler(deny_request)
        
        # API key is valid, continue with normal processing
        return await continuation(handler_call_details)
