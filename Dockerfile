FROM python:3.11
ENV PYTHONUNBUFFERED=true
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

CMD ["python3", "main.py"]
