# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

ARG DOPPLER_TOKEN
ENV DOPPLER_TOKEN=$DOPPLER_TOKEN

# Update and install dependencies
# Add Doppler's RSA key
RUN wget -q -t3 'https://packages.doppler.com/public/cli/rsa.8004D9FF50437357.key' -O /etc/apk/keys/cli@doppler-8004D9FF50437357.rsa.pub

# Add Doppler's apk repo
RUN echo 'https://packages.doppler.com/public/cli/alpine/any-version/main' | tee -a /etc/apk/repositories
RUN apk update && apk add --no-cache libffi-dev openssl-dev build-base curl doppler

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

# Install Gunicorn
RUN pip install gunicorn

# Run Gunicorn with 4 worker processes
CMD ["doppler", "run", "--", "gunicorn", "--workers=4", "--bind=0.0.0.0:3000", "app.main:app"]