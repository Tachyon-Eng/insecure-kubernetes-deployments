FROM node:16


RUN mkdir /app
WORKDIR /app


COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 3000


CMD ["/bin/bash", "-c", "node init_db.js && node server.js"]
