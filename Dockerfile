FROM python:3.9

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r requirements.txt

CMD ["python3", "src/main.py"]