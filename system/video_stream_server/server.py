import asyncio
import gi
import cv2
import numpy as np
import threading
from gi.repository import Gst, GLib

Gst.init(None)

ROOM = 'room'

class VideoStreamServer:
    def __init__(self, sio, ip):
        self.sio = sio
        self.ip = ip
        self.pipeline = Gst.Pipeline.new("video-stream-pipeline")
        self.tcp_client_src = Gst.ElementFactory.make("tcpclientsrc", "tcp_client_src")
        self.tcp_client_src.set_property("host", self.ip)
        self.tcp_client_src.set_property("port", 8888)

        self.h264_parser = Gst.ElementFactory.make("h264parse", "h264_parser")
        self.h264_decoder = Gst.ElementFactory.make("openh264dec", "h264_decoder")
        self.video_converter = Gst.ElementFactory.make("videoconvert", "video_converter")
        self.app_sink = Gst.ElementFactory.make("appsink", "app_sink")
        self.app_sink.set_property("emit-signals", True)
        self.app_sink.set_property("sync", False)
        self.app_sink.connect("new-sample", self.on_new_sample)

        if not all([self.tcp_client_src, self.h264_parser, self.h264_decoder, self.video_converter, self.app_sink]):
            raise Exception("Failed to create one or more GStreamer elements")

        self.pipeline.add(self.tcp_client_src)
        self.pipeline.add(self.h264_parser)
        self.pipeline.add(self.h264_decoder)
        self.pipeline.add(self.video_converter)
        self.pipeline.add(self.app_sink)

        self.tcp_client_src.link(self.h264_parser)
        self.h264_parser.link(self.h264_decoder)
        self.h264_decoder.link(self.video_converter)
        self.video_converter.link(self.app_sink)

    def on_new_sample(self, sink):
        sample = sink.emit("pull-sample")
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        width = caps.get_structure(0).get_value("width")
        height = caps.get_structure(0).get_value("height")
        format = caps.get_structure(0).get_value("format")

        print(f"Received frame: width={width}, height={height}, format={format}")

        success, mapinfo = buffer.map(Gst.MapFlags.READ)
        if not success:
            print("Buffer map failed")
            return Gst.FlowReturn.ERROR

        frame = np.ndarray(
            (height + height // 2, width),
            buffer=mapinfo.data,
            dtype=np.uint8,
        )

        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
        frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_180) # just becous it's upside down

        _, jpeg = cv2.imencode('.jpg', frame_bgr)
        frame_data = jpeg.tobytes()
        buffer.unmap(mapinfo)

        print(f"Sending frame of size: {len(frame_data)} bytes")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.emit_frame(frame_data))

        return Gst.FlowReturn.OK
    
    async def emit_frame(self, frame_data):
        await self.sio.emit('frame', frame_data, room=ROOM)

    def run(self):
        print("Starting server...")
        self.pipeline.set_state(Gst.State.PLAYING)
        loop = GLib.MainLoop()

        def start_loop():
            try:
                loop.run()
            except KeyboardInterrupt:
                self.pipeline.set_state(Gst.State.NULL)
                raise

        loop_thread = threading.Thread(target=start_loop, daemon=True)
        loop_thread.start()