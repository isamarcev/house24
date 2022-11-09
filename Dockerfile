FROM python:3.10

WORKDIR /usr/src/home24-main

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update \
#    && apt-get install netcat -y

#RUN apt-get update -y && apt-get install -y postgresql gcc python3-dev musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/home24-main/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/home24-main

#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
#RUN chmod +x /usr/src/app/entrypoint.sh


#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

