import asyncio
import json

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import (HTTPException, RequestValidationError)
from aio_pika.exceptions import AMQPException


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


@app.exception_handler(AMQPException)
async def amqp_exception_handler(_, exception):
    return response.error(constant.INTERNAL_SERVER_ERROR, str(exception))
