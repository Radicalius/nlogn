sed "s/==PORT==/$PORT/" /etc/nginx/nginx-template.conf > /etc/nginx/nginx.conf
nginx
gunicorn server:app -b 0.0.0.0:8000
