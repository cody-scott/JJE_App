# Do nginx details first

Need running nginx before this will work


# Get Yahoo credentials if needed

Set the info and callbacks to your app

    Callback Domain - myapp.herokuapp.com
    Redirect URI(s) - https://myapp.herokuapp.com/oauth/callback
    

# Create new db locally

    psql
    CREATE DATABASE app_new;
    
# Create a database on heroku

Follow steps on site for a new DB attached to instance

# Add environment variables

    AD_Email:            False
    DEBUG_COLLECTSTATIC: 1
    SECRET_KEY:          *
    SU_Email:            False
    Send_Email:          True
    client_id:           *
    client_sec:          *
    email_password:      *
    email_user:          *
    league_id:           nhl.l.*****

# create private_config.py file in JJE_App folder (for local only)

    database_url = 'postgres://user:password@localhost:5432/app_new'

# Create tables

    python manage.py migrate
    
# Create superuser

    python manage.py createsuperuser
    
# update Tables

### Sites table

change domain name to the target website 
    
    https://myapp.herokuapp.com
    
### Email table

add your email info to the email table

# Push to heroku

    heroku pg:push app_new DATABASE_URL -a appname
    
# Complete Yahoo Flow

This.

# Set your token in the token table to be the "standings token"

in admin view

# run teams flow

    https://myapp.herokuapp.com/standings/maketeams
    
# Link your team in the teams table

Manually attach your team to your user ID

OR 

Re-run yahoo auth flow, and update token table to be standings token

