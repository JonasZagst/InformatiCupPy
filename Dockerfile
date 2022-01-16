# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /InformatiCupPy

RUN pip3 install pandas

COPY . .

CMD ["python", "Main.py"]