FROM nginx

COPY requirements.txt requirements.txt

RUN apt-get update; \
apt-get install -y python3 python3-pip; \
python3 -m pip install -r requirements.txt

COPY proxy/nginx.conf /etc/nginx/nginx-template.conf
COPY start.sh /
COPY ./web /
COPY ./redirect redirect
COPY ./cache cache

CMD bash start.sh
