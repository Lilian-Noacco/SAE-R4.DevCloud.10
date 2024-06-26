# Dockerfile for Flask
FROM python:3.12

# Install necessary packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements.txt from the flask directory
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the rest of the Flask application
COPY . /app/

# Expose the required port
EXPOSE 5000

# Run the Flask server
CMD ["python", "main.py"]
