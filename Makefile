r:
	python manage.py runserver

m:
	python manage.py makemigrations && python manage.py migrate
user:
	python manage.py createsuperuser
mr:
	python manage.py makemigrations && python manage.py migrate && python manage.py runserver
celery:
	celery -A home24 worker --loglevel=INFO
