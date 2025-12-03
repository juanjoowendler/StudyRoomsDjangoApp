Useful links:

* Django documentation: https://www.djangoproject.com/
* Django documentation - User Model: https://docs.djangoproject.com/en/5.2/ref/contrib/auth/

Used commands:

* python manage.py migrate (at the beginning of the project and every time makemigrations is executed)
* python manage.py makemigrations (when we add models)
* python manage.py runserver
* python manage.py createsuperuser (create user and password to access the Django administration panel)
* django-admin startproject `<project_name>`
* django-admin startproject `<app_name>`

Django logic:

User → URLs → Views → Models → DB → Templates → Response
