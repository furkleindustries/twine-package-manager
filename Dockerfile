# Use the official Python 3.6 image as a base.
# https://hub.docker.com/_/python/
FROM python:3.6

# Give full colors in the output.
ARG TERM=xterm-256color

# Make the terminal non-interactive.
ARG DEBIAN_FRONTEND=noninteractive

# Create the directory for the server container.
RUN mkdir /etc/twine-package-manager-server/

# Set the working directory.
WORKDIR /etc/twine-package-manager-server/