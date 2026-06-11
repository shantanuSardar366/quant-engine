FROM ubuntu:22.04

# Install system dependencies including Python and C++ compiler
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all project files into the container
COPY . .

# Compile the C++ quantitative engine binary
RUN g++ -O3 quant_engine.cpp -o quant_engine

# Install Python frameworks and the MongoDB database drivers
RUN pip3 install --no-cache-dir flask requests pymongo dnspython

EXPOSE 8080

# Run the API gateway
CMD ["python3", "app.py"]
