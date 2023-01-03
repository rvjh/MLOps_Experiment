FROM python:3.9-slim

RUN pip freeze > requirements.txt

WORKDIR /app

COPY ["predict.py","test.py","web_service/lin_reg.bin","./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn","--bind=0.0.0.0:9696","predict:app"]



