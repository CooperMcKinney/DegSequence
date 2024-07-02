# Use the official Python image from the Docker Hub
FROM python:3.9

# Create a directory for the app
WORKDIR /workspace

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "Illumina_Analysis.py"]
