FROM python:3.9-alpine

WORKDIR /app

COPY scripts/scripts.py /app/scripts.py

RUN mkdir -p /home/data/output
COPY data/IF.txt /home/data/IF.txt
COPY data/AlwaysRememberUsThisWay.txt /home/data/AlwaysRememberUsThisWay.txt

CMD ["python", "/app/scripts.py"]