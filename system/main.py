import os
from dotenv import load_dotenv
import socketio
import uvicorn
from starlette.applications import Starlette
from video_stream_server.server import VideoStreamServer

ROOM = 'room'

load_dotenv('../utils/nvcam.conf')
ip = os.getenv("IP") # camera ip address

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
star_app = Starlette(debug=True)
app = socketio.ASGIApp(sio, star_app)

video_stream_server = VideoStreamServer(sio, ip)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('ready', room=ROOM, skip_sid=sid)
    await sio.enter_room(sid, ROOM)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    await sio.leave_room(sid, ROOM)

if __name__ == '__main__':
    try:
        video_stream_server.run()
        uvicorn.run(app, host='0.0.0.0', port=8003)
    except KeyboardInterrupt:
        pass
