from fastapi import APIRouter, WebSocket

from backend.app.events.manager import manager

router = APIRouter(prefix="/events", tags=["events"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast({"type": "event", "payload": data})
    except Exception:
        manager.disconnect(websocket)
