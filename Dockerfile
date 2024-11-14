FROM python:3.12-slim

WORKDIR /app

copy requirements.txt

RUN python.exe -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requiriments.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]