# CREATE BASEIMAGE --> BASED ON CURRENT CODING LANG
FROM python:3.13.1

# choose work directory (where to create app, usually /app or creates and /app folder)
# folder inside a container, and makes sure all of it goes inside /app as there are other folders
WORKDIR /app

# use '. .' to copy all files
# use 'filename' to just copy that file
# use '/dockerignore' to exclude files from copy

# input 1: source (. means all files)
# input 2: destination (. means whatever WORKDIR specifies, otherwise manually specify, e.g. /app/requirements.txt)
COPY . .

# use RUN to install all required dependencies for the app
RUN pip install -r requirements.txt
# here we just use -r requirements so it installs everything from the txt file

# use CMD to run the app!
# executed after the image (above code) has been run/made
CMD ["python", "app.py"]

# run in the terminal!

# docker build -t docker_ex1 . --> build the docker, give it a name (-t) and use the current workfolder (task1) as context
# docker run docker_ex1 --> run the docker and associated apps
# docker run --volume task1:/app DATA479Task1