FROM python:3.9-slim-buster

WORKDIR /code
COPY . .

RUN pip3 install rpyc

# ensure that the timezone within the containers is correctly set
RUN echo "Europe/Amsterdam" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata


ENTRYPOINT ["python", "-u", "./client.py"]
# ENTRYPOINT ["python", "-u", "./client_loop_symbols.py"]
