# JJE App

[![Build Status](https://travis-ci.org/namur007/JJE_App.svg?branch=master)](https://travis-ci.org/namur007/JJE_App)

## ***Setup***

Made for python 3.6

1. install requirements from pip

        pip install -r requirements.txt


1. Migrate the database

        python manage.py migrate


1. Create super user (Only needed if building from scratch)

        python manage.py createsuperuser

    This should be your email for the username + email


1. Set your environment variables

    email_user

        This is the email account to send info from

    email_password

        This is the password for the default emailer

    SECRET_KEY

        secret key for your application

    DATABASE_URL

        Database_url string for the application


### Making Oauth requests to yahoo

If you would like to make any requests that hit the yahoo api then you will need to do additional work

Examples of items that hit the api currently are the linking of the user to their teams in yahoo
and updating the current weekly standings.

Since these require requests be sent over HTTPS you will need to setup a reverse proxy using NGINX.

Additionally you will need to configure this proxy to serve a certificate you create to ensure its over https.

#### settings.py file

move these items outside the if block

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

#### Host file

Update your host file to include a url. ***www.myapp.new*** is what i used below.

#### NGINX Config example

Here is an example configuration. You will need to update paths below with your data.

Specifically update the ssl cert/ssl key paths and the log path

Update anything that says myapp.new to your path

finally update the proxy redirect

    # --------------------
    worker_processes  1;

    events {
        worker_connections  1024;
    }


    http {
        include       mime.types;
        default_type  application/octet-stream;

        sendfile        on;

        keepalive_timeout  65;

        server {
            listen 80;
            return 301 https://$host$request_uri;
        }

        server {
            listen 443;
            server_name www.myapp.new *.myapp.new;

            ssl_certificate "/usr/local/etc/nginx/ssl/myapp.crt";
            ssl_certificate_key "/usr/local/etc/nginx/ssl/myapp.key";

            ssl on;
            ssl_session_cache builtin:1000 shared:SLL:10m;
            ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
            ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
            ssl_prefer_server_ciphers on;

            access_log	"/Users/codyscott/tmp_logs/myapp.log";

            location / {
                    proxy_set_header        Host $host;
                    proxy_set_header        X-Real-IP $remote_addr;
                    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header        X-Forwarded-Proto $scheme;

                    # Fix the “It appears that your reverse proxy set up is broken" error.
                    proxy_pass          http://localhost:8000;
                    proxy_read_timeout  90;

                    proxy_redirect      http://localhost:8000 https://www.myapp.new;

            }
        }
    }


#### Run the server

    nginx start

then hit your link via the weblink. My example again is ***www.myapp.new***


Everything should redirect through https now.
