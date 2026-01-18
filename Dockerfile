# Dockerfile for the escape room.
# To build:
# `docker build -t my-escape-room:latest .`


FROM python:3.14

# Set the workdir to /app and copy and install the requirements
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the html files
COPY admin.html /app/admin.html
COPY index.html /app/index.html
COPY main.py /app/main.py

# Set the command that runs when the container starts
ENTRYPOINT ["python"]
CMD ["main.py"]