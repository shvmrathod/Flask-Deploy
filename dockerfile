# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only the required files
COPY requirements.txt /app/
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Add this to run your app
CMD ["python", "app.py"]