# Use a slim Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
