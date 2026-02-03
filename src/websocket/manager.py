import asyncio

from fastapi import WebSocket

from src.config import settings


class ConnectionManager:
    def __init__(self):
        self.ws_to_tags: dict[WebSocket, set[int]] = {}
        self.tag_to_ws: dict[int, set[WebSocket]] = {}
        self.ws_to_queue: dict[WebSocket, list[dict]] = {}
        self.ws_to_flush_task: dict[WebSocket, asyncio.Task] = {}

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.ws_to_tags[ws] = set()
        self.ws_to_queue[ws] = []

    def disconnect(self, ws: WebSocket):
        for tag_id in self.ws_to_tags.get(ws, set()):
            self.tag_to_ws.get(tag_id, set()).discard(ws)
            if tag_id in self.tag_to_ws and not self.tag_to_ws[tag_id]:
                del self.tag_to_ws[tag_id]
        self.ws_to_tags.pop(ws, None)
        self.ws_to_queue.pop(ws, None)
        task = self.ws_to_flush_task.pop(ws, None)
        if task:
            task.cancel()

    def subscribe(self, ws: WebSocket, tag_ids: list[int]):
        for tag_id in tag_ids:
            if tag_id not in self.ws_to_tags[ws]:
                self.ws_to_tags[ws].add(tag_id)
                if tag_id not in self.tag_to_ws:
                    self.tag_to_ws[tag_id] = set()
                self.tag_to_ws[tag_id].add(ws)

    async def broadcast_to_tag(self, tag_id: int, message: dict):
        if tag_id not in self.tag_to_ws:
            return
        for ws in list(self.tag_to_ws[tag_id]):
            if ws not in self.ws_to_queue:
                self.ws_to_queue[ws] = []
            self.ws_to_queue[ws].append(message)

            if ws not in self.ws_to_flush_task or self.ws_to_flush_task[ws].done():
                self.ws_to_flush_task[ws] = asyncio.create_task(self._flush(ws))

    async def _flush(self, ws: WebSocket):
        await asyncio.sleep(settings.BATCH_INTERVAL_MS / 1000.0)
        if ws in self.ws_to_queue and self.ws_to_queue[ws]:
            batch = self.ws_to_queue[ws]
            del self.ws_to_queue[ws]
            try:
                await ws.send_json(batch)
            except Exception:
                pass

    async def send_immediate(self, ws: WebSocket, message: dict):
        try:
            await ws.send_json([message])
        except Exception:
            pass


manager = ConnectionManager()
