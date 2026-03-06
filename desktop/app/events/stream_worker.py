import asyncio
from typing import Optional

from PySide6.QtCore import QThread, Signal
import websockets

class EventStreamWorker(QThread):
    event_received = Signal(object)
    error = Signal(Exception)

    def __init__(self, base_url: str, cookie_header: Optional[str] = None):
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.cookie_header = cookie_header
        self._running = True

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.listen())
        except Exception as exc:
            self.error.emit(exc)
        finally:
            loop.close()

    async def listen(self):
        ws_url = self.base_url.replace('http://', 'ws://').replace('https://', 'wss://').rstrip('/') + '/events/ws'
        headers = []
        if self.cookie_header:
            headers.append(('Cookie', self.cookie_header))
        try:
            async with websockets.connect(ws_url, extra_headers=headers) as ws:
                while self._running:
                    try:
                        message = await ws.recv()
                        self.event_received.emit(message)
                    except websockets.ConnectionClosedError:
                        break
                    except Exception as exc:
                        self.error.emit(exc)
                        await asyncio.sleep(3)
        except Exception as exc:
            self.error.emit(exc)

    def stop(self):
        self._running = False
