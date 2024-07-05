# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set default port in an environment variable
ENV PORT=8000

# Expose default port
EXPOSE $PORT

COPY . .

# Run the application using uvicorn. Use the PORT environment variable if provided.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]