# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (adjust based on your app.py)
EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]