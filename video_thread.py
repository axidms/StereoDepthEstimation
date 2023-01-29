import json
import cv2 as cv

from threading import Thread


class VideoThread(Thread):
    def __init__(self):
        super().__init__()

        front_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        self.__front_cam = cv.VideoCapture(front_udp_camera_pipe)

        left_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9203 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        self.__left_cam = cv.VideoCapture(left_udp_camera_pipe)

        right_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9204 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
        self.__right_cam = cv.VideoCapture(right_udp_camera_pipe)

        self.left_frame = None
        self.right_frame = None
        self.front_frame = None


    def run(self):
        while True:
            ret, frame = self.__front_cam.read()
            self.front_frame = frame

            ret, frame = self.__left_cam.read()
            self.left_frame = frame

            ret, frame = self.__right_cam.read()
            self.right_frame = frame
