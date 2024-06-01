import os
import time
from dotenv import load_dotenv
import socketio
import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from video_stream_server.server import VideoStreamServer

ROOM = 'room'

load_dotenv('../utils/nvcam.conf')
ip = os.getenv("IP") # camera ip address

# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['*'])
sio = socketio.AsyncServer(
    async_mode='asgi', 
    cors_allowed_origins=["http://localhost:5173"]
)

star_app = Starlette(debug=True)
star_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

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
        time.sleep(3)
        video_stream_server.run()
        uvicorn.run(app, host='0.0.0.0', port=8003)
    except KeyboardInterrupt:
        pass
