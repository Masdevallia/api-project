
FROM python:3.7-slim

# Copy the contents of the current directory inside the docker image:
ADD . /app

# Set the home of the docker image:
WORKDIR /app

# Install the requirements:
RUN pip3 install -r requirements.txt
RUN python3 nltkdownload.py

# Do not run the container in superuser mode:
RUN adduser --disabled-password myuser
USER myuser 

# Command to run when starting the container:
CMD ["python3","-u","api.py"]


# docker build -t chat-analysis-api .
# docker run chat-analysis-api
