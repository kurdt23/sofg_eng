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

RUN useradd -ms /bin/bash Jenkins

USER Jenkins
WORKDIR /home/Jenkins
