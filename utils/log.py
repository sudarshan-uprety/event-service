import asyncio
import logging
import uuid
from contextvars import ContextVar

import httpx

from utils.variables import ENV, LOKI_URL

# ContextVar to store the trace ID for the current context
trace_id_var = ContextVar("trace_id", default="")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.trace_id = trace_id_var.get()
        return super().format(record)


class AsyncLokiHandler(logging.Handler):
    def __init__(self, url, labels=None):
        super().__init__()
        self.url = url
        self.labels = labels or {}
        self.queue = asyncio.Queue()
        self.client = httpx.AsyncClient()
        self.task = asyncio.create_task(self.sender())

    async def sender(self):
        while True:
            record = await self.queue.get()
            try:
                await self.send_log(record)
            except Exception as e:
                print(f"Failed to send log to Loki: {e}")
            finally:
                self.queue.task_done()

    async def send_log(self, record):
        log_entry = self.format(record)
        payload = {
            "streams": [
                {
                    "stream": self.labels,
                    "values": [[str(int(record.created * 1e9)), log_entry]]
                }
            ]
        }
        headers = {'Content-type': 'application/json'}
        response = await self.client.post(self.url, json=payload, headers=headers)
        response.raise_for_status()

    def emit(self, record):
        asyncio.create_task(self.queue.put(record))

    async def close(self):
        await self.client.aclose()
        await self.queue.join()

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Loki handler
    loki_handler = AsyncLokiHandler(
        url=LOKI_URL,
        labels={"service": "login-auth", "env": ENV}
    )
    loki_handler.setLevel(logging.DEBUG)
    loki_formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s')
    loki_handler.setFormatter(loki_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(loki_handler)

    return logger


# Create a global logger instance
logger = get_logger("event_and_search_api")


def set_trace_id(trace_id=None):
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    trace_id_var.set(trace_id)
    return trace_id
