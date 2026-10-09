FROM python:3.9-slim

# Install required packages
RUN pip install kubernetes requests

# Create directory for callback results
RUN mkdir -p /app/results

# Copy client files
COPY ssh_client.py /app/
COPY listener.py /app/
WORKDIR /app

# Make scripts executable
RUN chmod +x /app/ssh_client.py /app/listener.py

# Default command - this will be overridden by the args in the deployment YAML
CMD ["bash", "-c", "python listener.py & python ssh_client.py"]
