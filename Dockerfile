# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

ARG DOPPLER_TOKEN
ENV DOPPLER_TOKEN=$DOPPLER_TOKEN

ARG DOPPLER_PROJECT
ENV DOPPLER_PROJECT=$DOPPLER_PROJECT

ARG DOPPLER_ENVIRONMENT
ENV DOPPLER_ENVIRONMENT=$DOPPLER_ENVIRONMENT

# Update and install dependencies
# Add Doppler's RSA key
RUN wget -q -t3 'https://packages.doppler.com/public/cli/rsa.8004D9FF50437357.key' -O /etc/apk/keys/cli@doppler-8004D9FF50437357.rsa.pub

# Add Doppler's apk repo
RUN echo 'https://packages.doppler.com/public/cli/alpine/any-version/main' | tee -a /etc/apk/repositories
RUN apk update && apk add --no-cache libffi-dev openssl-dev build-base curl doppler

# Install Supervisor
RUN apk add --no-cache supervisor

RUN mkdir /app

COPY pyproject.toml poetry.lock /app/

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 3000

# Define environment variables
ENV FLASK_APP=flask.py
ENV FLASK_ENV=production

# Install Gunicorn and Huey
RUN pip install gunicorn
RUN pip install huey

# Copy the Supervisor configuration file
COPY ./devops/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]