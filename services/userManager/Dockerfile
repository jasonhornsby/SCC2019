FROM node:13.0-alpine

# Add dependencies for the build
RUN apk add --no-cache --virtual .gyp python make g++

# Env
ENV NODE_ENV development

# Create Directory for the container
WORKDIR /usr/src/app

COPY package.json .
RUN npm install

ADD . /usr/src/app
RUN npm run compile

RUN /bin/sh
CMD [ 'npm', 'start']
EXPOSE 8000
