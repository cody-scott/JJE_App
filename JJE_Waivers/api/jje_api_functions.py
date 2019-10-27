from JJE_Waivers.models import WaiverClaim
from JJE_Main.utils import jje_main_functions
from JJE_Standings.utils import jje_standings_functions
from JJE_Waivers.utils import email_functions

from django.db import transaction


def validate_cancel_claim(request, pk):
    guid = request.user.usertoken_set.first().user_guid
    user_teams = jje_main_functions.get_users_teams_ids(guid)

    try:
        wc_obj = WaiverClaim.objects.get(id=pk)
    except:
        return ["Claim doesn't exist"], 400

    if wc_obj.yahoo_team.id not in user_teams:
        return ["Team ID is not valid for your login"], 400

    wc_obj.cancelled = True

    try:
        with transaction.atomic():
            wc_obj.save()
            email_functions.cancel_email(wc_obj, request)
            return wc_obj, 200

    except Exception as e:
        # save error
        return ["Problem with the request"], 500


def validate_new_claim(request, data):
    claim_data = parse_input_data(data)

    if None in [claim_data.get("yahoo_team_id")]:
        return ["Problem with input"], 400

    guid = request.user.usertoken_set.first().user_guid
    user_teams = jje_main_functions.get_users_teams_ids(guid)

    # validate claim team sent is a team of that users
    if not _is_claim_team_users(claim_data, user_teams):
        # not a users team, return exception
        return ["Team ID is not valid for your login"], 400

    claim_type = "New"

    new_claim = WaiverClaim()
    new_claim.yahoo_team_id = claim_data.get('yahoo_team_id')
    
    new_claim.add_player = claim_data.get("add_player")
    new_claim.add_LW = claim_data.get('add_LW')
    new_claim.add_C = claim_data.get('add_C')
    new_claim.add_RW = claim_data.get('add_RW')
    new_claim.add_D = claim_data.get("add_D")
    new_claim.add_G = claim_data.get("add_G")
    new_claim.add_Util = claim_data.get("add_Util")
    new_claim.add_IR = claim_data.get("add_IR")
    
    new_claim.drop_player = claim_data.get("drop_player")
    new_claim.drop_LW = claim_data.get('drop_LW')
    new_claim.drop_C = claim_data.get('drop_C')
    new_claim.drop_RW = claim_data.get('drop_RW')
    new_claim.drop_D = claim_data.get("drop_D")
    new_claim.drop_G = claim_data.get("drop_G")
    new_claim.drop_Util = claim_data.get("drop_Util")
    new_claim.drop_IR = claim_data.get("drop_IR")

    new_claim.claim_message = claim_data.get("claim_message")

    try:
        with transaction.atomic():
            new_claim.save()
            email_functions.send_waiver_email(new_claim, "New Claim", request)
            return new_claim, 200

    except Exception as e:
        # save error
        return ["Problem with the request"], 500


def validate_over_claim(request, data):
    claim_data = parse_input_data(data)

    if None in [claim_data.get("yahoo_team_id"), claim_data.get('over_claim_id')]:
        return ["Problem with input"], 400

    guid = request.user.usertoken_set.first().user_guid
    user_teams = jje_main_functions.get_users_teams_ids(guid)

    if not _is_claim_team_users(claim_data, user_teams):
        # not a users team, return exception
        return ["Team ID is not valid for your login"], 400

    wc_obj = WaiverClaim.objects.filter(id=data["over_claim_id"])  # type: WaiverClaim
    if len(wc_obj) == 0:
        return ["Not a valid overclaim ID"], 400
    wc_obj = wc_obj[0]
    wc_team_id = wc_obj.yahoo_team.id

    # validate if it is an overclaim
    if not wc_obj.active_claim():
        # error not valid
        return ["Claim ID is not active"], 400

    if not _is_valid_overclaim(claim_data['yahoo_team_id'], wc_team_id):
        # claim team isn't in overclaim teams
        return ["Cannot overclaim. Not ranked higher"], 400

    # flag existing claim as overclaimed
    wc_obj.overclaimed = True
    
    # create new claim
    new_claim = WaiverClaim()
    new_claim.yahoo_team_id = claim_data.get('yahoo_team_id')
    
    new_claim.add_player = wc_obj.add_player
    new_claim.add_LW = wc_obj.add_LW
    new_claim.add_C = wc_obj.add_C
    new_claim.add_RW = wc_obj.add_RW
    new_claim.add_D = wc_obj.add_D
    new_claim.add_G = wc_obj.add_G
    new_claim.add_Util = wc_obj.add_Util
    new_claim.add_IR = wc_obj.add_IR

    new_claim.drop_player = claim_data.get("drop_player")
    new_claim.drop_LW = claim_data.get('drop_LW')
    new_claim.drop_C = claim_data.get('drop_C')
    new_claim.drop_RW = claim_data.get('drop_RW')
    new_claim.drop_D = claim_data.get("drop_D")
    new_claim.drop_G = claim_data.get("drop_G")
    new_claim.drop_Util = claim_data.get("drop_Util")
    new_claim.drop_IR = claim_data.get("drop_IR")

    new_claim.claim_message = claim_data.get("claim_message")

    new_claim.over_claim_id = wc_obj.id

    try:
        with transaction.atomic():
            new_claim.save()
            wc_obj.save()
            email_functions.send_waiver_email(new_claim, "Overclaim", request)

            return new_claim, 200

    except Exception as e:
        # save error
        return ["Problem with the request"], 500


def _is_claim_team_users(data, user_ids):
    if data['yahoo_team_id'] in user_ids:
        return True
    else:
        return False


def _is_overclaim(data):
    if data.get("over_claim_id") == 0:
        return False
    else:
        return True


def _is_valid_overclaim(claimee_id, wc_team_id):
    # these are the teams the requested user CAN overclaim
    overclaim_teams = jje_standings_functions.get_overclaim_teams([claimee_id])
    if wc_team_id in overclaim_teams:
        return True
    else:
        return False


def parse_input_data(data):
    yahoo_team_id = _parse_team_id(data.get("yahoo_team", None))

    add_player = data.get("add_player", None)

    add_LW = data.get("add_LW", False)
    add_C = data.get("add_C", False)
    add_RW = data.get("add_RW", False)
    add_D = data.get("add_D", False)
    add_G = data.get("add_G", False)
    add_Util = data.get("add_Util", False)
    add_IR = data.get("add_IR", False)

    drop_player = data.get("drop_player", None)

    drop_LW = data.get("drop_LW", False)
    drop_C = data.get("drop_C", False)
    drop_RW = data.get("drop_RW", False)
    drop_D = data.get("drop_D", False)
    drop_G = data.get("drop_G", False)
    drop_Util = data.get("drop_Util", False)
    drop_IR = data.get("drop_IR", False)

    over_claim_id = _parse_overclaim(data.get("over_claim_id", None))

    claim_message = data.get("claim_message", "")
    
    return {
        "yahoo_team_id": yahoo_team_id,

        "add_player": add_player,
        "add_C": add_C,
        "add_RW": add_RW,
        "add_LW": add_LW,
        "add_D": add_D,
        "add_G": add_G,
        "add_Util": add_Util,
        "add_IR": add_IR,
        
        "drop_player": drop_player,
        "drop_C": drop_C,
        "drop_RW": drop_RW,
        "drop_LW": drop_LW,
        "drop_D": drop_D,
        "drop_G": drop_G,
        "drop_Util": drop_Util,
        "drop_IR": drop_IR,

        "over_claim_id": over_claim_id,

        "claim_message": claim_message,
    }


def _parse_team_id(team_id):
    try:
        return int(team_id)
    except:
        # todo error checking
        return None


def _parse_overclaim(over_claim_data):
    try:
        if over_claim_data == '':
            over_claim_id = 0
            return over_claim_id

        over_claim_id = int(over_claim_data)
        return over_claim_id
    except:
        return None
