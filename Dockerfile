FROM python:3.8-slim

WORKDIR /app

# Download Libraries
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app into working directory
COPY ./app .

# Expose ports
EXPOSE 8080

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api:app"]
