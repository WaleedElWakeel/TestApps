import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os
from redis import Redis
redis_client = Redis.from_url(
    os.environ.get('REDIS_URL'), decode_responses=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI()


async def heavy_data_processing(data: dict):
    """Some (fake) heavy data processing logic."""
    await asyncio.sleep(2)
    message_processed = data.get("message", "").upper()
    return message_processed


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the connection from a client.
    await websocket.accept()

    while True:
        try:
            # Receive the JSON data sent by a client.
            data = await websocket.receive_json()
            # Some (fake) heavey data processing logic.
            message_processed = await heavy_data_processing(data)
            # Send JSON data to the client.
            await websocket.send_json(
                {
                    "state": 0,
                    "message": message_processed,
                    "date": datetime.now().isoformat(),
                    "isRead": False,
                    "link": 'test link'
                }
            )
        except WebSocketDisconnect:
            logger.info("The connection is closed.")
            break


@app.get("/env", response_model=str, status_code=200)
async def get_env():
    return os.getenv('TEST_ENV')


@app.get("/redis", response_model=str, status_code=200)
async def get_cache():
    value = redis_client.get('test_key')
    if not value:
        print("Not cached")
        value = 'data'
        redis_client.set('test_key', value)

    return value
