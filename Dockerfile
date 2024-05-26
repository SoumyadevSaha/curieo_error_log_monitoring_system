# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container (no need for this case)
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt (no need for this case)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Command to run the Python script
CMD ["python", "log_monitor.py"]
