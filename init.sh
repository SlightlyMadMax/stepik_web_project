sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo rm -rf /etc/nginx/sites-enabled/default
sudo nginx -t
sudo /etc/init.d/nginx restart

gunicorn -c /home/box/web/etc/gunicorn.conf ask.wsgi:application