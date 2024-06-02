import os
import glob
import time
from dotenv import load_dotenv
import socketio
import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from video_stream_server.server import VideoStreamServer
import base64

ROOM = 'room'

load_dotenv('../utils/nvcam.conf')
ip = os.getenv("IP") # camera ip address

# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['*'])
sio = socketio.AsyncServer(
    async_mode='asgi', 
    cors_allowed_origins=["http://localhost:5173"]
)

async def get_images(request):
    page = request.path_params['page']
    images_per_page = 10
    start = (page - 1) * images_per_page
    end = start + images_per_page

    image_files = sorted(glob.glob('./images/*.jpg'))
    paginated_files = image_files[start:end]

    if not paginated_files:
        return JSONResponse(status_code=404, content={"detail": "No images found for this page."})

    encoded_images = []
    for image_file in paginated_files:
        with open(image_file, 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
            encoded_images.append(encoded_string)

    return JSONResponse({'images': encoded_images})

star_app = Starlette(debug=True, routes=[Route('/page/{page:int}', get_images, methods=['GET']),])
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
