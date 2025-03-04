# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY . .

# Install the dependencies
RUN pip install "uvicorn[standard]"
RUN pip install -e .

# command to run 
CMD ["uvicorn", "sciwyrm.main:app", "--host", "0.0.0.0"]
