FROM python:3

WORKDIR ./src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD [ "gunicorn", "-b","0.0.0.0:5000","wsgi:app" ]
