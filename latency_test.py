import cv2 as cv
from datetime import datetime


front_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
front_cam = cv.VideoCapture(front_udp_camera_pipe)

while True:

   ret, frame = front_cam.read()
   frame = cv.flip(frame, 0)
   frame = cv.flip(frame, 1)

   now = datetime.now()

   current_time = now.strftime("%M:%S")
   print(current_time)

   frame = cv.putText(frame, current_time, (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

   cv.imwrite("latency.jpeg", frame)

