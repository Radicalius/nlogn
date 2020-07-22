sed "s/==PORT==/$PORT/" /etc/nginx/nginx-template.conf > /etc/nginx/nginx.conf
nginx
python scheduler.py &
gunicorn server:app -b 0.0.0.0:8000
