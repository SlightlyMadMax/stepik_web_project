sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo rm -rf /etc/nginx/sites-enabled/default
sudo nginx -t
sudo /etc/init.d/nginx restart

gunicorn wsgi.ask:application --bind 0.0.0.0:8000