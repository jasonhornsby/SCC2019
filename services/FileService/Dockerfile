# Dockerfile

# Pull base image
FROM python:3.6

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /code
WORKDIR /code

# Dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
EXPOSE 5000


CMD python app.py
# alternativ: CMD flask run [--host 172.17.0.2]