# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
# You should list all your dependencies in the requirements.txt file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Jupyter and nbconvert
RUN pip install jupyter nbconvert

# Install MinIO client
RUN pip install minio

# Install dotenv to load environment variables
RUN pip install python-dotenv

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Run Jupyter notebook on container startup
CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]
