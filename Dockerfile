# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
ADD ./app/requirements.txt /var/www/requirements.txt
RUN pip install --no-cache-dir -r /var/www/requirements.txt

# Copy project files
COPY ./app/ /var/www/
WORKDIR /var/www

# Expose port
EXPOSE 8000

# Start server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
