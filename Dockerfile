FROM python:3.12
WORKDIR /usr/src
RUN mkdir app
COPY ./ ./app
WORKDIR /usr/src/app
RUN rm -r .venv
RUN pip install --no-cache-dir -r requirements.txt