# Base Python Docker image
FROM python:3.9.5-buster

# Copy code into the container
COPY . /code

# Set the working directory
WORKDIR /code

# Install dependencies
RUN pip install -r req.txt

# Expose the port
EXPOSE 5001

# Run the Python file
CMD ["python", "main.py"]
