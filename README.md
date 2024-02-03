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
Figure it out.

### Docker Compose
```shell
# Start the DB and Redis :)
docker-compose up -d
```

### Install requirements
```shell
poetry install --with dev
```

## How to run locally (requires env vars)
```shell
poetry run python manage.py runserver
```

## How to run locally with doppler
```shell
doppler run -- poetry run python manage.py runserver
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