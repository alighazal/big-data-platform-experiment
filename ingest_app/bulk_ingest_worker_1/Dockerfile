FROM python:3.9.16-buster
WORKDIR /app
COPY . . 
RUN python -m pip install --upgrade pip
RUN pip install -r ./requirments.txt
CMD [ "python3", "app.py" ]