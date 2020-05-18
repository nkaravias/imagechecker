FROM python:3

WORKDIR /opt/imagechecker

COPY imagechecker/ .
COPY conf/ .
COPY requirements.txt .

RUN pip install -r requirements.txt && \
apt-get update -y && \
apt-get install -y vim \
&& apt clean all

CMD ["python", "/opt/imagechecker/main.py", "-c", "/opt/imagechecker/etc/config.yaml"]