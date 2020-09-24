# Django-DiaryWritting-Project
A responsive web app built with Django 3.0.5. Multiple users can write diary on their Profile.
***
## Features
- Multiple user login and signup.
- Diary writing functionality.
- Only the uploaded user can view their written stuff on their profile after login.
***
## Requirements
- Django = 3.0.5
- python = 3.7.3
- django-crispy-forms = 1.9.0
- Pillow = 7.1.2
- djangorestframework = 3.11.0
***
## INSTALLED_APPS
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diary',
    'landingpage',
    'crispy_forms',
    'rest_framework'
]
```
***
## urls.py
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landingpage.urls')),
    path('diary/',include('diary.urls')),
    path('', include('pwa.urls')),
    url(r'^books/',views.book_view.as_view()),
    url(r'^feeds/',views.feed_view.as_view()),
    url(r'^profiles/',user_views.profile_view.as_view()),

    
    
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```
***
## How to run it
- to migrate the database
```
$ cd mindnote
$ python manage.py makemigrations
$ python manage.py migrate
```
- to run the program
```
python manage.py runserver
```
Copy the IP address provided once your server has completed building the site. (It will say something like >> Serving at 127.0.0.1....).Open the address in the browser
***
## Project Tree
```
├── mindnote
    ├── landingpage
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── migrations
    │   ├── tests.py
    │   ├── forms.py
    │   └── tokens.py
    │   ├── urls.py
    │   ├── serializer.py
    │   └── views.py
    │
    ├── db.sqlite3
    ├── manage.py
    │
    ├── media   
    │   └── uploads
    │
    ├── mindnote
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── static
    │   └── icons
    │   └── manifest.webmanifest
    │   └── mindnote
    │       ├── css
    │       ├── js
    │       ├── fonts
    │       ├── img
    │
    ├── templates
    │   ├── diary
    │   ├── landingpage
    │       ├── serviceworker.js
    │
    ├── diary
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── migrations
    │   ├── tests.py
    │   ├── forms.py
    │   ├── serializer.py
    │   ├── urls.py
    │   └── views.py
 ```
