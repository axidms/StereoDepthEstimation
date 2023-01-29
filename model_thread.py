import json
import cv2 as cv

from threading import Thread
from hitnet import HitNet, ModelType


class ModelThread(Thread):
    def __init__(self):
        super().__init__()

        model_type = ModelType.eth3d
        model_path = "models/eth3d/saved_model_120x160/model_float16_quant.tflite"

        self.__hitnet_depth = HitNet(model_path, model_type)


    def run(self):
        while True:
            ret, frame = self.__front_cam.read()
            self.front_frame = frame

            ret, frame = self.__left_cam.read()
            self.left_frame = frame

            ret, frame = self.__right_cam.read()
            self.right_frame = frame
