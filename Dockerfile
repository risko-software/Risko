FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
COPY requirements.txt .
RUN pip install -r requirements.txt

# Permite correr en modo debug para ver las trazas de error
ENV MODE_DEBUG=False

#Permite establecer el contexo donde estara corriendo la app, ejemplo: <>/<>/<>/
ENV CONTEXT_RISKO_APP="risko/"

ENV DEFAULT_NAME=""
ENV DEFAULT_USER=""
ENV DEFAULT_PASSWORD=""
ENV DEFAULT_HOST=""
ENV DEFAULT_PORT=""

#riesgos
ENV RIESGOS_NAME=""
ENV RIESGOS_USER=""
ENV RIESGOS_PASSWORD=""
ENV RIESGOS_HOST=""
ENV RIESGOS_PORT=""

#base
ENV BASE_NAME=""
ENV BASE_USER=""
ENV BASE_PASSWORD=""
ENV BASE_HOST=""
ENV BASE_PORT=""

#email
ENV EMAIL_HOST=""
ENV EMAIL_PORT=""
ENV EMAIL_HOST_USER=""
ENV EMAIL_HOST_PASSWORD=""

RUN mkdir /var/log/risko_log
VOLUME /var/log/risko_log

EXPOSE 8080

ENTRYPOINT ["python3", "./manage.py", "runserver", "0.0.0.0:8080"]