# Poločas nápadu API

> Defender of the [Poločas nápadu](https://polocas-napadu.cz) database

This project provides API for systems of the Prague based theatre improvisation group Poločas nápadu. It is based on Django and uses Graphql as a frontend.

## Install

```sh
poetry install
```

## Run locally

```sh
poetry run ./manage.py runserver
```

## Test

```sh
poetry run pytest
```

To run in watch mode:

```sh
poetry run pytest --watch
```

To generate coverage:

```sh
poetry run pytest --cov-report=xml --cov-config=.coveragerc --cov="."
```
