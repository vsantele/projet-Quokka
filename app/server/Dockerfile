FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./data/algoSVD.pkl /code/data/algoSVD.pkl
COPY ./app /code/app
COPY ../../dist/quokka /code/quokka

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]