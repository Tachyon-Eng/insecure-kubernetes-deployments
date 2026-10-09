FROM python:3.9-slim


RUN pip install kubernetes requests


RUN mkdir -p /app/results


COPY ssh_client.py /app/
COPY listener.py /app/
WORKDIR /app


RUN chmod +x /app/ssh_client.py /app/listener.py


CMD ["bash", "-c", "python listener.py & python ssh_client.py"]
