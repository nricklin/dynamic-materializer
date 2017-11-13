FROM tdgp/gdal

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN yum install -y unzip
RUN python /get-pip.py
RUN pip install -y boto3
RUN pip install -y tiletanic
RUN pip install -y boto3
ADD dynamic.py /dynamic.py
ADD task.py /task.py

CMD python /task.py