FROM centos:8

RUN yum install -y python3-pip
RUN pip3 install web.py

COPY jokes.json serve.py ./

CMD exec python3 -u serve.py
