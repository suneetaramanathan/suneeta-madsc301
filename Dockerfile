# Use official Python image
FROM python:3.10-slim

# Install cron and pip
RUN apt-get update && \
    apt-get install -y cron && \
    pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Copy and install crontab
COPY crontab.txt /etc/cron.d/etl-cron
RUN chmod 0644 /etc/cron.d/etl-cron && \
    crontab /etc/cron.d/etl-cron

# Start cron and Jupyter
CMD cron && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
