# cpc-tooling
Webhooks for CPC, written in Python.

## Requirements
- Poetry
- Python3.10
- Doppler CLI
  - Access to our secrets too
- Docker (if you want to run it in a container)

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