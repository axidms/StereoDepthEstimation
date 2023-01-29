from functools import reduce
from hitnet import HitNet, ModelType
import random
import cv2 as cv
import socket

from video_thread import VideoThread

def get_min_max_depth(image, hitnet_depth):
    #result, image = cam.read()
    
    if image is None:
        print(f"No image detected. Please! try again")
        return 0, 0

    image = cv.flip(image, 0)
    #cv.imwrite("flip.jpeg", image)

    h, w, channels = image.shape

    half = w//2
            
    h = 120
    w = 160
    dim = (w, h)

    left_img = image[:, :half]
    left_img = cv.resize(left_img, dim, interpolation=cv.INTER_NEAREST)

    right_img = image[:, half:]
    right_img = cv.resize(right_img, dim, interpolation=cv.INTER_NEAREST)

    h_save_space = int(h*0.50)

    left_img = left_img[0:h-h_save_space, 0:half]
    right_img = right_img[0:h-h_save_space, 0:half]

    # Estimate the depth

    disparity_map = hitnet_depth(left_img, right_img)

    rmin, rmax, rMinPoint, pMaxPoint = cv.minMaxLoc(disparity_map, None)

    p = 85.0/100.0

    max_depth = (100 - rmin*10)*p
    min_depth = (100 - rmax*10)*p

    print(f"Max: {max_depth}, Min: {min_depth}")

    return max(0, min_depth), max(0, max_depth)


def get_distance(video_thread, hitnet_depth):
    front_min, front_max = get_min_max_depth(video_thread.front_frame, hitnet_depth)
    left_min, left_max = get_min_max_depth(video_thread.left_frame, hitnet_depth)
    right_min, right_max = get_min_max_depth(video_thread.right_frame, hitnet_depth)

    return front_min, left_min, right_min


def server():
    model_type = ModelType.eth3d
    model_path = "models/eth3d/saved_model_120x160/model_float16_quant.tflite"

    hitnet_depth = HitNet(model_path, model_type)

    #front_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    #front_cam = cv.VideoCapture(front_udp_camera_pipe)

    #left_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9203 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    #left_cam = cv.VideoCapture(left_udp_camera_pipe)

    #right_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9204 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    #right_cam = cv.VideoCapture(right_udp_camera_pipe)

    video_thread = VideoThread()
    video_thread.start()


    host = "192.168.123.14"
    port = 5001
    
    print(f"Server: {host}:{port}")

    server_socket = socket.socket()
    server_socket.bind((host, port))

    print("Waiting for connection...")

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))

        if str(data) == "all":
            front_min, left_min, right_min = get_distance(video_thread, hitnet_depth)
            data = f"{front_min};{left_min};{right_min}"
            print("sending: " + data)
            conn.send(data.encode())
        elif str(data) == "front":
            front_min, front_max = get_min_max_depth(video_thread.front_frame, hitnet_depth)
            data = f"{front_min}"
            print("sending: " + data)
            conn.send(data.encode())
        elif str(data) == "left":
            left_min, left_max = get_min_max_depth(video_thread.left_frame, hitnet_depth)
            data = f"{left_min}"
            print("sending: " + data)
            conn.send(data.encode())
        elif str(data) == "right":
            right_min, right_max = get_min_max_depth(video_thread.right_frame, hitnet_depth)
            data = f"{right_min}"
            print("sending: " + data)
            conn.send(data.encode())

if __name__ == '__main__':
    server()
