FROM python:3.11.4-slim-buster

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential curl libpq-dev --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && mkdir -p /home/python/.cache/pip && chown python:python -R /home/python /app

USER python

COPY --chown=python:python requirements.txt requirements.txt

RUN pip3 install --no-cache-dir  --user -r requirements.txt

COPY --chown=python:python bot/ ./bot

ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python config.py launch.py ./

EXPOSE 443 80 88 8443

CMD ["python", "launch.py"]
