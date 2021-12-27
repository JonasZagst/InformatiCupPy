FROM python:3

WORKDIR /InformatiCupPy

COPY . .

CMD ["python", "/InformatiCupPy/InformatiCupPy/com/informaticup/python/Main.py"]