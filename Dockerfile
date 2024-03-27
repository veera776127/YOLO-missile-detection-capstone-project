# Use the latest official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install libGL for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade ultralytics

# Set appropriate permissions for the directories
RUN chmod -R 777 /app/uploads /app/results

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app1.py when the container launches
CMD ["python", "app1.py"]
