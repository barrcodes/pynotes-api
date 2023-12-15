FROM python:3.9-slim-buster
WORKDIR /app
ADD . /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 80
