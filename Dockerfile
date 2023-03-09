FROM python:3.11.2-slim-bullseye

ENV PYTHONUNBUFFERED=true
ENV DEBIAN_FRONTEND=noninteractive

ARG APP_DIR=/app
ARG PROJECT_DIR=./sine_wave_producer
ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR $APP_DIR

COPY $REQUIREMENTS_FILE $REQUIREMENTS_FILE

RUN pip3 install --upgrade --no-input --no-cache-dir pip \
    && pip3 install --upgrade --no-input --no-cache-dir --requirement $REQUIREMENTS_FILE \
    && rm --recursive --force /root/.cache/pip \
    && rm $REQUIREMENTS_FILE

COPY $PROJECT_DIR .

ENTRYPOINT ["python3"]
CMD ["main.py"]
