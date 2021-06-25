FROM ubuntu

WORKDIR /app
RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]