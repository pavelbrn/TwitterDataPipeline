FROM python:3.6

WORKDIR /etl

COPY . /etl

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "etl.py"]