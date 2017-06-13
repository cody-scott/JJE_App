# JJE App

[![Build Status](https://travis-ci.org/namur007/JJE_App.svg?branch=master)](https://travis-ci.org/namur007/JJE_App)

## ***Setup***

Made for python 3.6

1. install requirements from pip

        pip install -r requirements.txt


1. Migrate the database

        python manage.py migrate

    Fill in any blanks if they appear with some default value. Delete those afterwards

1. Create super user (Only needed if building from scratch)

        python manage.py createsuperuser

    This should be your email for the username + email


1. Set your environment variables

    email_password
    email_user
    SECRET_KEY


1. Do all your fun stuff!

