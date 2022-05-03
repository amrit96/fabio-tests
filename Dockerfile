FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install

COPY . .

ENV PORT=5002

CMD [ "python"]