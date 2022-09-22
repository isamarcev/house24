r:
	python manage.py runserver

m:
	python manage.py makemigrations && python manage.py migrate
user:
	python manage.py createsuperuser