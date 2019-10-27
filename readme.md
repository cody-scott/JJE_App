
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
    
    
## Start chrome

    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ignore-certificate-errors &> /dev/null &
    
    
    
## API

## Token access

Request token with 

    api/token/
    
    data = {"username": "", "password"}
    
    returns "access" and "refresh" token
    
Refresh token with

    api/token/refresh/
    
    data = {"refresh": "<refresh token>"

#### Headers to add to requests

    {"Authorization": "Bearer <TOKEN>"}

### Waiver claim api

team ID info

    /api/teams

Active Claim info

    waivers/api/active_claims/

### Submitting claims

Claims should be sent as POST

-----

**Create New claim**

    /waivers/api/new
    data = {
        "yahoo_team": 9,
        "add_player": "testadd",
        "add_IR": True,
        "drop_player": "testdrop",
        "drop_D": True,
    }
    
**Overclaim**

    /waivers/api/overclaim
    data = {
        "yahoo_team": 9,
        "over_claim_id": 36,
        "drop_player": "testdrop",
        "drop_D": True,
    }
    
    
**Cancel**

supply cancellation ID in the url

    /waivers/api/cancel/<ID>



### Yahoo Player Data

**Individual Player Stats**

    /oauth/api/player/

    data {
        'player_id': 6381,
    }
    requests.get("./oauth/api/player", headers=headers, params=data)
    
**Collection of Player Stats**
    
/oauth/api/players/

full list of parameters

https://developer.yahoo.com/fantasysports/guide/#players-collection

    data {
        'status': "FA",
        "position": "C",
        "sort_type": "lastweek",
        "sort": "AR",
    }
    requests.get("./oauth/api/players", headers=headers, params=data)