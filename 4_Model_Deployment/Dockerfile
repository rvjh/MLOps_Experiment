FROM python:3.9-slim

WORKDIR /app

COPY ["requirements.txt","predict.py","test.py","lin_reg.bin","./"]

RUN pip install -r requirements.txt

EXPOSE 9696

ENTRYPOINT ["gunicorn","--bind=0.0.0.0:9696","predict:app"]



