# Download base image ubuntu 22.04
FROM ubuntu:22.04

# LABEL about the custom image
LABEL maintainer="organismus22@gmail.com"
LABEL version="1.0"
LABEL description="docker agent for jenkins"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update

RUN apt-get update && apt-get install -y \
  git \
  subversion \
  make \
  vim \
  mc \
  python3 \
  python3-venv \
  python3-pip \
  flex \
  gawk \
  zip \
  bison

# Create Jenkins user
RUN useradd -ms /bin/bash Jenkins

# Switch to Jenkins user
USER Jenkins

# Set the working directory
WORKDIR /home/Jenkins

# Copy the repository contents into the container
COPY . .

# Install Python dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt

# Download the pre-trained model
RUN . venv/bin/activate && pip3 install gdown && gdown https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt -O yolov8n.pt

# Modify the config file
RUN sed -i 's|path: \x27./video.mp4\x27|path: \x270\x27|' config.yaml