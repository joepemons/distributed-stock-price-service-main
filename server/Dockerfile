FROM python:3.9-slim-buster

WORKDIR /code
COPY . .

RUN pip3 install rpyc
RUN pip3 install yfinance

# ensure that the timezone within the containers is correctly set
RUN echo "Europe/Amsterdam" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# EXPOSE 5000
CMD ["python", "-u", "./server.py"]
