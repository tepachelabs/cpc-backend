# cpc-webhooks
Webhooks for CPC, written in Python.

## Requirements
- Poetry
- Python3.10
- Doppler CLI
  - Access to our secrets too
- Docker (if you want to run it in a container)

## How to run locally (requires env vars)
```shell
PYTHONPATH=$(pwd) poetry run python app/main.py
```

## How to run locally with doppler
```shell
PYTHONPATH=$(pwd) doppler run -- poetry run python app/main.py
```

## How to test
```shell
# TODO write tests
```

## How to deploy
Should be done automatically by github actions.

## License
[MIT](./LICENSE)