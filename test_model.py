from hitnet import HitNet, ModelType
import cv2 as cv

model_type = ModelType.eth3d
model_path = "models/eth3d/saved_model_120x160/model_float16_quant.tflite"

hitnet_depth = HitNet(model_path, model_type)

print(hitnet_depth)

left_img = cv2.imread("left.jpg", cv2.IMREAD_UNCHANGED)
right_img = cv2.imread("right.jpg", cv2.IMREAD_UNCHANGED)

left_img = cv2.resize(left_img, dim, interpolation=cv2.INTER_NEAREST)
right_img = cv2.resize(right_img, dim, interpolation=cv2.INTER_NEAREST)

h_save_space = int(h*0.30)

left_img = left_img[0:h-h_save_space, 0:half]
right_img = right_img[0:h-h_save_space, 0:half]

disparity_map = hitnet_depth(left_img, right_img)

rmin, rmax, rMinPoint, pMaxPoint = cv2.minMaxLoc(disparity_map, None)

p = 85.0/100.0

max_depth = (100 - rmin*10)*p
min_depth = (100 - rmax*10)*p

print(f"Max: {max_depth}, Min: {min_depth}")