FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && pip install --upgrade pip

RUN pip install requests pystac

COPY /src/read_write_stac.py /app/

RUN chmod +x /app/read_write_stac.py
