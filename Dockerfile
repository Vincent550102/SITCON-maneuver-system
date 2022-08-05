FROM python:3.8 
USER root
RUN pip install pipenv; 

WORKDIR /app
COPY . .
RUN pipenv install --ignore-pipfile --system --deploy
ENTRYPOINT python app.py
