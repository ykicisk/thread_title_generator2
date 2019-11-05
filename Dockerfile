FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04 

LABEL maintainer "ykic.p3@gmail.com"

ARG UID
ARG GID

# install apt packages
RUN apt-get update && \
  apt-get -y install python3 python3-dev python3-distutils python3-setuptools \
  gcc sudo language-pack-ja mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file \
  libhdf5-serial-dev

# install neologd
RUN mkdir /install
WORKDIR /install
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /install/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y -p "/usr/share/mecab/dic/mecab-ipadic-neologd"

# install python packages
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python3
RUN pip install jupyterlab lxml emoji tensorflow-gpu tensorflow-datasets sklearn mecab-python3


# locale setting
RUN update-locale LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8

# add docker user
RUN groupadd -g $GID docker
RUN useradd -m --uid $UID --gid $GID --shell /bin/bash docker

# WORKDIR
WORKDIR /home/docker
ENV HOME /home/docker

EXPOSE 8889
