FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p downloads cache raw_files

# Run the bot
CMD ["python3", "main.py"]