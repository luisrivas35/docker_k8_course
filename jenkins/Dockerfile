# Use the official Jenkins image from Docker Hub
FROM jenkins/jenkins:latest

# Switch to the root user to perform system-level operations
USER root

# Install additional packages - OpenSSH server, Nano, and Docker
RUN apt-get update && apt-get install -y openssh-server nano
RUN curl -fsSL https://get.docker.com | sh

# Download tini using curl
RUN curl -fsSL -o /sbin/tini https://github.com/krallin/tini/releases/download/v0.19.0/tini
RUN chmod +x /sbin/tini

# Create a directory for mounting the volume
RUN mkdir -p /mnt/c/curso_devops/docker/jenkins

# Expose ports 8080, 50000, and 22
EXPOSE 8080 50000 22

# Change the working directory
WORKDIR /var/jenkins_home

# Entry point for running Jenkins with tini
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/jenkins.sh"]
