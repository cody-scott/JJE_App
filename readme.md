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

----

### Making Oauth requests to yahoo

Need to have ssl server locally. Setup with nginx

#### NGINX Config example

see nginx_setup folder for nginx, host file, and ssl setup.


#### Run the server

    nginx start

then hit your link via the weblink. My example again is ***www.myapp.test***

----


# FOR DEVELOPMENT

Setup nginx and environment variables

# New Season

1. Swap sites to local dev. ie: https://www.myapp.test
2. Swap token info to development token

### Delete existing data from these tables

1. yahoostanding
2. waiverclaim
3. yahooteam
4. oauth_usertoken



### Test
1. Add your token (do flow)
1. Assign your token to "standings" token
1. Load teams from yahoo https://www.myapp.test/standings/maketeams
1. manually assign your team to the correct one
1. run a waiver claim

#### Chrome testing

for chrome, need security toned down.

        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ignore-certificate-errors &> /dev/null &


#### Fix Stuff

Stuff broken? Fix it up!

-----


### Working?

Delete data from following again

1. oauth_usertoken
2. yahooteam
3. yahoostanding

        DELETE from "JJE_Waivers_waiverclaim";
        DELETE from "JJE_Waivers_yahooteam";
        DELETE from "JJE_oauth_usertoken";
        DELETE from "JJE_Standings_yahoostanding";

----

### Push to Heroku

    heroku pg:push {localdbname} DATABASE_URL -a {APPNAME}
    
### Recommended

Create a test DB on the server and test against that to be safe


### ENV Variables

    DEBUG = True -> flag for debugging. usually true for local development
    EMAIL_HOST_USER -> email of league email
    EMAIL_HOST_PASSWORD -> password of league email. Should be single app generated, not master password
    client_id -> client id for site from yahoo. Should be local development for www.myapp.new
    client_secret -> client secret for site from yahoo. Should be local development for www.myapp.new
    LEAGUE_ID = 'nhl.l.xxxxx' -> nhl league id. replace xxxxx with id
    SU_Email = True -> flag to email superuser only
    AD_Email = False -> flag to email admin only
    Send_Email = True -> flag to send email
    
    
### For yahoo

set the sites table in the db

exp https://www.myapp.test