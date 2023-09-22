# cpc-webhooks
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
PYTHONPATH=$(pwd) poetry run python app/main.py
```

## How to run locally with doppler
```shell
PYTHONPATH=$(pwd) doppler run -- poetry run python app/main.py
```

## How to test
Currently using `unittest` to write tests, nothing fancy just to fix bugs that appears from time to time.

```shell
doppler run -- poetry run python -m unittest
```

## How to deploy
Should be done automatically by github actions.

## License
[MIT](./LICENSE)