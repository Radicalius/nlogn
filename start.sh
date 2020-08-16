sed "s/==PORT==/$PORT/" /etc/nginx/nginx-template.conf > /etc/nginx/nginx.conf
nginx
python3 cache/server.py 10000 &
python3 redirect/server.py 9000 &
python3 server.py 8000
