FROM arm32v7/python:3.7

COPY . /app

RUN pip install --user poetry
RUN apt-get install sense-hat

WORKDIR /app
RUN /root/.local/bin/poetry install

RUN python main.py
