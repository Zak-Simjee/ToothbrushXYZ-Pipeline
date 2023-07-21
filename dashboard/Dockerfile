FROM python:3.10
WORKDIR /app

ADD requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED True

CMD ["python", "app.py"]