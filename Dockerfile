# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install g++ compiler inside the cloud container
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Flask
RUN pip install --no-cache-dir flask

# Compile the C++ engine inside Linux container environment
RUN g++ quant_engine.cpp -o quant_engine.exe

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]