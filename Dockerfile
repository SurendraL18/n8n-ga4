FROM node:18-slim

WORKDIR /data

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl git && \
    apt-get clean

COPY ./scripts/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

RUN npm install -g n8n

EXPOSE 5678
ENTRYPOINT ["n8n"]
