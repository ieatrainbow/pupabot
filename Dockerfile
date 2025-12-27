FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/
RUN mkdir -p data
RUN apt update && apt install -y ffmpeg && apt clean && apt autoclean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 pupa && \
    chown -R pupa:pupa /usr/src/app
USER pupa

CMD ["python3", "src/main.py"] 