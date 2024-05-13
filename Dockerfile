# Use an official Python runtime as a parent image
FROM python:3.9

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD ["python","-u","src/flightplan.py"]