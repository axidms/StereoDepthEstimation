import cv2 as cv
from datetime import datetime
from hitnet import HitNet, ModelType


front_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
front_cam = cv.VideoCapture(front_udp_camera_pipe)

model_type = ModelType.eth3d
model_path = "models/eth3d/saved_model_120x160/model_float16_quant.tflite"

hitnet_depth = HitNet(model_path, model_type)


while True:
    ret, image = front_cam.read()

    now = datetime.now()
    print(now.strftime("frame read:  %S %f"))

    image = cv.flip(image, 0)
    image = cv.flip(image, 1)

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

    now = datetime.now()
    print(now.strftime("frame processing:  %S %f"))

    disparity_map = hitnet_depth(left_img, right_img)

    now = datetime.now()
    print(now.strftime("disparity map:  %S %f"))

    rmin, rmax, rMinPoint, pMaxPoint = cv.minMaxLoc(disparity_map, None)

    p = 85.0/100.0

    max_depth = (100 - rmin*10)*p
    min_depth = (100 - rmax*10)*p

    print(f"Max: {max_depth}, Min: {min_depth}")

    now = datetime.now()
    print(now.strftime("finish:  %S %f"))
