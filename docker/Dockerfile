# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application's source code into the container
COPY . .

# Expose the port the application will run on (if applicable)
EXPOSE 8000

# Define environment variables for your application (if needed)
# ENV EXAMPLE_VAR=example_value

# Command to run your application
CMD ["python", "app.py"]
