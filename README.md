Geocoder: Geocode excel sheets with google geocoding api
=========================

Setup
------------

Install requiremens

    $ sudo pip install -r requirements.txt

Run migrations

    $  python manage.py migrate

Start celery worker

    $ celery worker -A geocoder

Start development server

    $ python manage.py runserver
