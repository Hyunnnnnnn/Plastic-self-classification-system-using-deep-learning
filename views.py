# camera/views.py

from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

def index(request):
    return render(request, 'camera/index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)  # 웹캠 인덱스 0 사용
        if not self.video.isOpened():
            raise Exception("Could not open video device")
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            raise Exception("Could not read frame from video device")
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
