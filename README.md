# cpc-backend
Backend for all CPC related apps, written in Python.

## Requirements
- Poetry
- Python3.10
- Doppler CLI
  - Access to our secrets too
- Docker (if you want to run it in a container)
- Redis (for CRON jobs)

## For macOS devs:
```shell
brew install poetry
brew install python@3.10
brew install doppler
brew install libpq # install only the postgresql libs not fully (if you want to use docker)

## This might be different.
sudo ln -s $(brew --prefix)/opt/libpq/bin/psql /usr/local/bin/psql
```

## For Others:
Figure it out yourself, or ask for help.

### Docker Compose
```shell
# Start the DB and Redis :)
docker-compose up postgres redis -d
```

### Install requirements
```shell
poetry install --with dev
```

# Recommendations when working with this repository

1. Run with doppler (many environment variables are required)
2. Run locally
3. Run infra with docker-compose
4. Test manually with your own telegram bot

## How to run the django app locally
```shell
poetry run python manage.py runserver
```

## How to run the django app locally with doppler
```shell
doppler run -- poetry run python manage.py runserver
```

## How to run the celery worker
```shell
# for some reason on macOS: 
#   you need to run this command with the --pool=solo
# on production it runs without it
doppler run -- poetry run celery -A cpc worker --loglevel=info --pool=solo
````

## How to run the telegram bot?
```shell
doppler run -- poetry run python manage.py run_telegram_bot
```

## With Docker Compose
**BEWARE:** Requires a doppler token, get it from doppler.
```shell
docker-compose up app
```

## How to test
Currently using `unittest` to write tests, nothing fancy just to fix bugs that appears from time to time.

```shell
doppler run -- poetry run python manage.py test
```

## How to deploy
Should be done automatically by github actions.

## License
[MIT](./LICENSE)