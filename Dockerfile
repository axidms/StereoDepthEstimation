FROM ubuntu:20.04


RUN apt-get update
RUN apt-get upgrade -y

# Install gstreamer and opencv dependencies
RUN \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

RUN \
	apt-get install -y \
	libgstreamer1.0-0 \
	gstreamer1.0-plugins-base \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav \
	gstreamer1.0-doc \
	gstreamer1.0-tools \
	libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev \
    wget \
    curl \
    build-essential \
    libssl-dev \
    cmake \
    gcc \
    g++ \
    git \
    python3 \
    python3-pip \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    nano \
    net-tools \
    netcat

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir numpy

RUN git clone https://github.com/opencv/opencv.git

RUN \
	cd opencv && \
	git checkout 4.5.4 && \
	git submodule update --recursive --init && \
	mkdir build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D PYTHON_EXECUTABLE=$(which python3) \
	-D BUILD_opencv_python2=OFF \
	-D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
	-D PYTHON3_EXECUTABLE=$(which python3) \
	-D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
	-D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
	-D WITH_GSTREAMER=ON \
	-D BUILD_EXAMPLES=ON ..

RUN cd opencv/build && make -j2 && make install && ldconfig

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt

COPY . /root/stereo_depth_estimation

ENV PYTHONPATH "${PYTHONPATH}:/root/stereo_depth_estimation"
WORKDIR /root/stereo_depth_estimation/

CMD ["/bin/bash"]