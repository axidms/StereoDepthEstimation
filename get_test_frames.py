import cv2 as cv

print(cv.getBuildInformation())

print("front")
front_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9201 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
front_cam = cv.VideoCapture(front_udp_camera_pipe, cv.CAP_GSTREAMER)

print("left")
left_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9203 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
left_cam = cv.VideoCapture(left_udp_camera_pipe, cv.CAP_GSTREAMER)

print("right")
right_udp_camera_pipe = "udpsrc address=192.168.123.14 port=9204 ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
right_cam = cv.VideoCapture(right_udp_camera_pipe, cv.CAP_GSTREAMER)

front_ret, front_frame = front_cam.read()

print(f"{front_ret} {front_frame}")

if front_frame is not None:
    cv.imwrite("front.jpeg", front_frame)

left_ret, left_frame = left_cam.read()

print(f"{left_ret} {left_frame}")

if left_frame is not None:
    cv.imwrite("left.jpeg", left_frame)

right_ret, right_frame = right_cam.read()

print(f"{right_ret} {right_frame}")

if right_frame is not None:
    cv.imwrite("right.jpeg", right_frame)
