FROM python:3.11.6-slim

ENV LANG C.UTF-8

# Copy application files and install dependencies.
WORKDIR /app
COPY . /app

# Install system packages and clean up.
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip3 install --no-cache-dir --upgrade -r requirements.txt && \
    chmod u+x deploy.sh

# Set the command to run your Python application.
#! NOTE: Use Gunicorn or another WSGI server built to run Flask apps in production instead of the internal Werkzeug server!
ENTRYPOINT ["./deploy.sh"]