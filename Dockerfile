FROM python:3.9-slim

# Set the working directory
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
