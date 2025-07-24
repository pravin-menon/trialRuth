# Use a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "main.py"]
# Docker command to delete everything inclduing cache
 
