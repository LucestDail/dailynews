nohup gunicorn --bind 0.0.0.0:8080 dailynews.wsgi:application &
tail -f nohup.out