FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY task.py ./
COPY config.py ./
RUN chmod +rwx ./task.py
RUN chmod +rwx ./config.py
#RUN python3 ./task.py
ENTRYPOINT ./task.py

