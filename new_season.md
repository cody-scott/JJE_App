# New Season

## Variables to set

Update the league_id variable
Update the starting week variable


## Cleanup

Can choose to  wipe the tables if you want.

wipe

* standings
* waiver claims
* yahoo user tokens
* yahoo guids
* yahoo_teams

Don't need to wipe user table, that can be reused

## .env variables

Set these variables on heroku and in a .env file for testing

    # postgres url for the database
    DATABASE_URL=""

    # django apps secret key
    SECRET_KEY=""

    # Info from yahoo app
    client_id=""
    client_secret=""

    # fantasy specific info
    league_id=""
    starting_week="2019-10-04"

    email_user=""
    email_password=""

    # For local development
    DJANGO_SETTINGS_MODULE="JJE_App.settings"
    DEBUG="TRUE"

    EMAIL_LEVEL="SUPER_USER"

    # if you don't want to send an email
    SEND_EMAIL="False"

    # This flags a creation/work on a local sqlite file instead of the postgres db
    LOCAL_WORK="TRUE"


## Start chrome

    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ignore-certificate-errors &> /dev/null &


