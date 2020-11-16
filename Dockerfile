# syntax=docker/dockerfile:1.0.0-experimental

FROM alpine:edge
 ENV CHARSET UTF-8
 ENV LANG C.UTF-8
 ENV LC_COLLATE C
 ENV TERM xterm-256color
 CMD ["sh","-il"]
 RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
 RUN apk --no-cache upgrade
 RUN apk --no-cache add \
  build-base \
  crystal \
  htop \
  mc \
  ncdu \
  nginx \
  nodejs-current \
  npm \
  openssl-dev \
  poetry \
  postgresql \
  postgresql-dev \
  python3-dev \
  shards \
  sqlite-dev \
  su-exec \
  tmux \
  uwsgi \
  uwsgi-http \
  uwsgi-python3 \
  yaml-dev \
  yarn \
  zlib-dev
 RUN ln -s /usr/bin/python3 /usr/bin/python
 RUN yarn global add \
  @angular/cli \
  @loopback/cli \
  @quasar/cli \
  @vue/cli \
  local-web-server \
  sails &&\
  rm -rf /usr/local/share/.cache /tmp/*
COPY dockerfs/ /
