
FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /order_pickup

# Set the working directory to /order_pickup
WORKDIR /order_pickup

# Copy the current directory contents into the container at /order_pickup
ADD . /order_pickup/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt