# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /InformatiCupPy

COPY . .

CMD ["python", "Main.py"]