# Use a lightweight Python 3.9 image
FROM python:3.11-slim

# Set our working directory
WORKDIR /app

# Copy only requirements first (leverages layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code into the image
COPY . .

# Default command: run the EDA script
CMD ["python", "eda.py"]