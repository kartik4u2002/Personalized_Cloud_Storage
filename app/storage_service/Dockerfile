# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /storage_service

# Copy only requirements first (for caching dependencies)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the image
COPY . .

# Create uploads folder
RUN mkdir uploads

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
