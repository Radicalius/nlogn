sed "s/==PORT==/$PORT/" /etc/nginx/nginx-template.conf > /etc/nginx/nginx.conf
nginx
python3 server.py 8000
