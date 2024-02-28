FROM python:3.12 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY ./docs  /code/docs
COPY ./.env.example  /code
COPY ./alembic.ini  /code
COPY ./.gitignore  /code
COPY ./README.md  /code
COPY ./main.py  /code




CMD ["python", "main.py"]