FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -d /home/python python \
    && mkdir -p /home/python/.cache/pip \
    && chown -R python:python /home/python /app

USER python

COPY --chown=python:python requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt --no-warn-script-location

COPY --chown=python:python tab/ ./tab
COPY --chown=python:python launch.py ./

ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"


EXPOSE 443 80 88 8443

CMD ["python", "launch.py"]