# JJE App

Application for the JJE Fantasy league

Handles waiver claims, standings emails and logic

See new_season.md for notes on how to setup a new season

## API

## Token access

Request token with 

    api/token/
    
    data = {"username": "", "password"}
    
    returns "access" and "refresh" token
    {'access': '<TOKEN>', 'refresh': '<TOKEN>'}
    
Refresh token with

    api/token/refresh/
    
    data = {"refresh": "<refresh token>"}

#### Headers to add to requests

Use access token as a header in your request

    {"Authorization": "Bearer <ACCESS_TOKEN>"}

## Waiver claim api

team ID info

    /api/teams

    For only your teams
    params={
        'user_teams': 1
    }
    requests.get('./api/teams', params=params, headers=headers)

Active Claim info

    waivers/api/active_claims/

### Submitting claims

New claims should be sent as POST
Cancel claims should be sent as PUT

-----

**Create New claim**

    /waivers/api/new/
    data = {
        "yahoo_team": 9,
        "add_player": "testadd",
        "add_IR": True,
        "drop_player": "testdrop",
        "drop_D": True,
    }
    
    requests.post('./waivers/api/new/', headers=headers, data=data)
    
**Overclaim**

    /waivers/api/overclaim/
    data = {
        "yahoo_team": 9,
        "over_claim_id": 36,
        "drop_player": "testdrop",
        "drop_D": True,
    }
    requests.post('./waivers/api/overclaim/', headers=headers, data=data)
    
    
**Cancel**

supply cancellation ID in the url

    /waivers/api/cancel/<ID>/
    requests.put('./waivers/api/cancel/<ID>/', headers=headers)

----

## Yahoo Player Data

**Individual Player Stats**

    /oauth/api/player/

    data {
        'player_id': 6381,
    }
    requests.get("./oauth/api/player/", headers=headers, params=data)
    
**Collection of Player Stats**
    
/oauth/api/players/

full list of parameters

https://developer.yahoo.com/fantasysports/guide/#players-collection

    /oauth/api/players/
    data {
        'status': "FA",
        "position": "C",
        "sort_type": "lastweek",
        "sort": "AR",
    }
    requests.get("./oauth/api/players/", headers=headers, params=data)
