# Dockerfile for ConvertRocket Backend
# Python 3.11 Slim Image
FROM python:3.11-slim

# Install system dependencies including FFmpeg, Ghostscript, and Node.js
# FFmpeg: video/audio conversions
# Ghostscript: advanced PDF tools  
# Node.js: REQUIRED by yt-dlp 2026+ for YouTube JS challenge solving (Shorts + many videos)
# curl + ca-certificates: needed to fetch NodeSource setup script
RUN apt-get update && \
    apt-get install -y ffmpeg ghostscript curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

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
