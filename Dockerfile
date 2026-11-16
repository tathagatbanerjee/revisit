FROM node:24.11.1-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg python3 python3-venv openssh-client ca-certificates && rm -rf /var/lib/apt/lists/*
COPY core-pipeline/requirements-preparation.txt /tmp/requirements-preparation.txt
RUN python3 -m venv /opt/preparation && /opt/preparation/bin/pip install --no-cache-dir -r /tmp/requirements-preparation.txt
WORKDIR /opt/revisit
COPY app/package.json app/package-lock.json ./app/
RUN cd app && npm ci --omit=dev && npm cache clean --force
COPY app ./app
COPY examples ./examples
COPY docs ./docs
COPY core-pipeline ./core-pipeline
COPY scripts ./scripts
RUN mkdir /data && chown node:node /data
USER node
ENV REVISIT_DATA=/data HOST=0.0.0.0 PORT=4320 REVISIT_PREP_PYTHON=/opt/preparation/bin/python
EXPOSE 4320
CMD ["node", "app/server.mjs"]
