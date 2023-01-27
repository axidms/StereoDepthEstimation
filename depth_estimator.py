from functools import reduce
from hitnet import HitNet, ModelType
import random
import cv2 as cv
import socket

def get_min_max_depth(cam, hitnet_depth):
    result, image = cam.read()

    if not result:
        print("No image detected. Please! try again")
        return
    
    h, w, channels = image.shape

    half = w//2
    
    h = 120
    w = 160
    dim = (w, h)

    left_img = frame_image[:, :half]
    left_img = cv2.resize(left_img, dim, interpolation=cv2.INTER_NEAREST)

    right_img = frame_image[:, half:]
    right_img = cv2.resize(right_img, dim, interpolation=cv2.INTER_NEAREST)

    h_save_space = int(h*0.30)

    left_img = left_img[0:h-h_save_space, :]
    right_img = right_img[0:h-h_save_space, :]

    # Estimate the depth

    disparity_map = hitnet_depth(left_img, right_img)

    rmin, rmax, rMinPoint, pMaxPoint = cv2.minMaxLoc(disparity_map, None)

    p = 85.0/100.0

    max_depth = (100 - rmin*10)*p
    min_depth = (100 - rmax*10)*p

    print(f"Max: {max_depth}, Min: {min_depth}")

    return min_depth, max_depth


def get_distance(front_cam, left_cam, right_cam, hitnet_depth):
    front_min, front_max = get_min_max_depth(front_cam, hitnet_depth)
    left_min, left_max = get_min_max_depth(left_cam, hitnet_depth)
    right_min, right_max = get_min_max_depth(right_cam, hitnet_depth)

    return front_min, left_min, right_min


def server():
    model_type = ModelType.eth3d
    model_path = "models/eth3d/saved_model_120x160/model_float32.tflite"

    hitnet_depth = HitNet(model_path, model_type)

    front_udp_camera_pipe = "udpsrc address=192.168.123.13 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! omxh264dec ! videoconvert ! appsink"
    front_cam = cv.VideoCapture(front_udp_camera_pipe)

    left_udp_camera_pipe = "udpsrc address=192.168.123.13 port=9203 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! omxh264dec ! videoconvert ! appsink"
    left_cam = cv.VideoCapture(left_udp_camera_pipe)

    right_udp_camera_pipe = "udpsrc address=192.168.123.13 port=9204 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! omxh264dec ! videoconvert ! appsink"
    right_cam = cv.VideoCapture(right_udp_camera_pipe)

    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))

        if str(data) == "min_distance":
            front_min, left_min, right_min = get_distance(front_cam, left_cam, right_cam, hitnet_depth)
            data = f"{front_min};{left_min};{right_min}"
            print("sending: " + data)
            conn.send(data.encode())

if __name__ == '__main__':
    server()
