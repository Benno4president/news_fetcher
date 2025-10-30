# syntax=docker/dockerfile:1
# Builder stage: install Python packages into a venv
FROM ubuntu:22.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      python3 python3-venv python3-pip build-essential && \
    rm -rf /var/lib/apt/lists/*

# create virtual environment and install requirements
RUN python3 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

WORKDIR /src
COPY requirements.txt /src/

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Runner stage: minimal runtime image
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Install python + Chromedriver
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    	python3 python3-venv 
		
# Create unprivileged user and copy venv from builder
RUN useradd --create-home --shell /bin/bash myuser
COPY --from=builder /home/myuser/venv /home/myuser/venv

USER myuser
WORKDIR /home/myuser/code

# Copy application source
COPY --chown=myuser:myuser . /home/myuser/code

ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

CMD ["python3", "news_scraper/main.py"]
