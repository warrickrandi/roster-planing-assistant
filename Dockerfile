# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port streamlit runs on
EXPOSE 8888

# Run dbconnect.py and crew_member.py to set up the database before running the Streamlit app
RUN python dbconnect.py
RUN python crew_member.py

# Run streamlit when the container launches
CMD ["streamlit", "run", "--server.port", "8888", "app.py"]
