# Base image with CUDA support
FROM nvidia/cuda:12.6.0-cudnn-runtime-ubuntu22.04

# Set non-interactive mode for apt to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get -o Acquire::AllowInsecureRepositories=true update && \
    apt-get install -y libxcb-xfixes0 libxcb-shape0 || true && \
    apt-get install -y --no-install-recommends ffmpeg curl || true && \
    apt --fix-broken install -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=300s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
