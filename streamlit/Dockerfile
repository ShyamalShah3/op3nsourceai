# Use an official Python runtime as the base image
FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy streamlit files to WORKDIR
COPY .streamlit/ /app/.streamlit/
COPY src/ /app/src

# Expose the port on which Streamlit will run (default is 8501)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit application
CMD ["streamlit", "run", "src/Home.py", "--server.port", "8501"]