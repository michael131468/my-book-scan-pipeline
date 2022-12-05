FROM fedora:37

RUN dnf install -y \
    https://rpms.remirepo.net/fedora/remi-release-37.rpm \
    https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-37.noarch.rpm

RUN dnf install -y \
    ImageMagick7 \
    ImageMagick7-heic \
    tesseract \
    fbida \
    scantailor \
    python3 \
    python3-pip \
    opencv-devel \
    opencv \
    eigen3 \
    git \
    make \
    gcc \
    gcc-c++

RUN pip3 install sh

RUN git clone https://github.com/jbarth-ubhd/fix-perspective.git
RUN cd fix-perspective && make && make install

RUN git clone 'https://github.com/tesseract-ocr/tessdata_best.git'

RUN mkdir -p /originals /output

ADD script.py /

ENTRYPOINT /bin/bash
