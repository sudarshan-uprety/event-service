import asyncio
import json

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import (HTTPException, RequestValidationError)

from utils import response, helpers, constant, exceptions, consumer
from routers import router

app = FastAPI(
    title="FastAPI Event Consumer and Full Text Search API",
    description="This service consumes messages from RabbitMQ queues and have API for full text search.",
    docs_url="/api/docs/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router)


# async def consume_messages():
#     while True:
#         try:
#             credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
#             connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials))
#             channel = connection.channel()
#
#             # Declare the queues
#             channel.queue_declare(queue=EMAIL_QUEUE, durable=True)
#             channel.queue_declare(queue=INVENTORY_QUEUE, durable=True)
#             channel.queue_declare(queue=PAYMENTS_QUEUE, durable=True)
#
#             # Set prefetch count for fair dispatch
#             channel.basic_qos(prefetch_count=2)
#
#             # Start consuming messages
#             channel.basic_consume(queue=EMAIL_QUEUE, on_message_callback=email_service_callback, auto_ack=False)
#             channel.basic_consume(queue=INVENTORY_QUEUE, on_message_callback=inventory_service_callback, auto_ack=False)
#             channel.basic_consume(queue=PAYMENTS_QUEUE, on_message_callback=payment_service_callback, auto_ack=False)
#
#             channel.start_consuming()
#         except (AMQPConnectionError, AMQPChannelError) as e:
#             print(f"RabbitMQ connection error: {e}. Retrying in 5 seconds...")
#             await asyncio.sleep(5)
#         except Exception as e:
#             print(f"Unexpected error: {e}. Retrying in 5 seconds...")
#             await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumer.consume_rabbitmq())


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return response.error(exception.status_code, exception.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exception):
    errors = helpers.pydantic_error(exception.errors())['body']
    msg = "Invalid data."
    return response.error(constant.UNPROCESSABLE_ENTITY, msg, errors)


@app.exception_handler(exceptions.GenericError)
async def generic_exception_handler(_, exception):
    return response.error(message=exception.message, status_code=exception.status_code)


@app.exception_handler(exceptions.InternalError)
async def internal_exception_handler(_, exception):
    return response.error(exception.status_code, exception.message)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return response.error(exception.status_code, exception.detail)


@app.exception_handler(json.JSONDecodeError)
async def json_exception_handler(_, exception):
    return response.error(constant.UNPROCESSABLE_ENTITY, str(exception))
