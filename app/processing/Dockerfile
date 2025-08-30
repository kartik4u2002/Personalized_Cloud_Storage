#Use the official Python 3.9 image as the base image
FROM python:3.9-slim-buster

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the working directory
COPY requirements.txt .

#Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application code into the working directory
COPY app.py .

#Expose port 5000, as Flask runs on this port by default
EXPOSE 5000

#Command to run the application
CMD ["python", "app.py"]