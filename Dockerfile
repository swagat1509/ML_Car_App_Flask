
FROM python:3.10.2
COPY . /usr/app1/
EXPOSE 5000
WORKDIR /usr/app1/
RUN pip install pip==21.2.4
RUN pip install -r requirements.txt
CMD python app.py 