# Dockerfile for ConvertRocket Backend
# Python 3.9 Slim Image
FROM python:3.9-slim

# Install system dependencies including FFmpeg
# This is crucial for video/audio conversions
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads converted downloads bin

# Expose port (Render uses port 10000 by default, or $PORT)
ENV PORT=8000
EXPOSE 8000

# Start command
# Uses uvicorn to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
