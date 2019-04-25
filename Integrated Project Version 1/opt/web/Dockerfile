FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y python3-pip python3-dev build-essential python3-tk
WORKDIR /home/dharshini/opt/web/
COPY . /home/dharshini/opt/web/
COPY requirements.txt /home/dharshini/opt/web/requirements.txt
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]