from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from src.websocket.manager import manager

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "subscribe":
                tags = data.get("tags", [])
                manager.subscribe(websocket, tags)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
