FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip

RUN pip install flask dynamsoft_barcode_reader_bundle uwsgi

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "app", "--master", "--processes", "4", "--logto", "/dev/stdout", "--limit-post", "104857600", "--socket-timeout", "600", "--harakiri", "600"]
