#!/bin/bash

sudo docker build -t stereo_depth_estimation_image_dev:latest -f Dockerfile .

sudo docker rm -f stereo_depth_estimation_dev

sudo docker run -it --name stereo_depth_estimation_dev --gpus all \
    --ipc=host --net=host stereo_depth_estimation_image_dev:latest
