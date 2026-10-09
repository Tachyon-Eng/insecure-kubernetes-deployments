
FROM ubuntu:20.04


ENV DEBIAN_FRONTEND=noninteractive


ENV SCRIPT_NAME=/app


RUN apt-get update && \
    apt-get install -y python3 python3-pip curl apt-transport-https ca-certificates software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir /app
WORKDIR /app


COPY app.py /app/
COPY requirements.txt /app/
COPY templates /app/templates/


RUN python3 -m pip install --no-cache-dir -r requirements.txt


RUN mkdir /uploads


RUN python3 -m pip install Flask

CMD ["python3", "/app/app.py"]
