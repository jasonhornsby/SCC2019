FROM node:alpine

# Add dependencies for the build
RUN apk add --no-cache --virtual .gyp python make g++

# Env
ENV NODE_ENV development

# Create Directory for the container
WORKDIR /usr/src/app

COPY package.json .
COPY tsconfig.json .
RUN npm install

ADD . /usr/src/app
RUN npm run compile
RUN ls -r ./dist

CMD ["npm", "start"]
EXPOSE 8000
