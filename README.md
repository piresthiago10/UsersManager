# Users Manager

 A small API to manage users in a company

 # Team:

* **Thiago Pires** - *Backend Developer*;

## System Requirements:

* Python 3.6;
* Django 3.1.7;
* Django Rest Framework 3.12.2

## Overview:

To create an ordinary user you must have create a super-user and log in to the api, create a department and then be able to create a common user informing the department id.

## Project Setup:

```
    1. Download or clone this repository
    2. Create the virtual environment:
        python3 - m venv venv
        source venv/bin/activate
    3. Install the requirements:
        pip install -r requirements.txt
    4. Make migrations and migrate:
        python3 manage.py makemigrations
        python3 manage.py migrate
    5. Create a Super-user:
        python3 manage.py createsuperuser
    6. Run the project:
        python manage.py runserver
```

## Run tests:
```
    1. In the virtual environment:
    python manage.py test
```

## Token Authentication:

This API uses Token Authentication.

This authentication scheme uses a simple token-based HTTP Authentication scheme. Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.

## API Documentation:

* [API Documentation](https://documenter.getpostman.com/view/7662540/TzCL98jc)    

## Tools

* [Visual Studio Code](https://code.visualstudio.com/)
* [Google Chrome](https://www.google.pt/intl/pt-PT/chrome/?brand=CHBD&gclid=Cj0KCQjwn_LrBRD4ARIsAFEQFKt3kLTIsdU6a-sk3FKsxrhplkKaYNHo6Pt3aRbaEAJ3TK4fZslZmtUaAvHVEALw_wcB&gclsrc=aw)
* [Postman](https://www.postman.com/)
