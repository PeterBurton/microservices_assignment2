# Use Python 3.6 runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run front_end.py when the container launches
CMD ["python", "front_end.py"]

# Expose port 3000 for the web app
EXPOSE 3000