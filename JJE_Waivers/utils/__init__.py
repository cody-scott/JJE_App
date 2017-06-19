from JJE_Standings.models import YahooStanding
from JJE_Waivers.models import YahooTeam


def get_user_teams_list(user):
    out_dct = {}
    teams = YahooTeam.objects.filter(user=user.id)
    if len(teams) == 1:
        out_dct = {'team': teams[0].id}
    return out_dct


def get_current_ranks(user):
    """Gets all the teams that are not eligible for overclaim"""
    ranks = []
    for item in user.yahooteam_set.all():
        ranks.extend([z.rank for z in item.yahoostanding_set.filter(current_standings=True).all()])

    rank = 0
    if len(ranks) > 0:
        rank = max(ranks)

    teams = [team.team.id for team in YahooStanding.objects.filter(current_standings=True, rank__gte=rank)]
    return teams


def get_claim_rank(team):
    standings = [item.rank for item in team.yahoostanding_set.filter(current_standings=True).all()]
    return standings


def show_oauth_link(request):
    """If both pass aka have a link, then dont show oauth link (AKA False)"""
    user = request.user
    if user.is_anonymous:
        return False

    # Enable this to ensure the user has a team AND token set
    # if not _check_user_token(user):
    #     return True

    # Enable this to ensure the user has a team assigned from yahoo
    # if not, it will provide yahoo oauth link instead
    if not _check_user_team(user):
        return True

    return False


def _check_user_token(user):
    if len(user.usertoken_set.all()) == 0:
        return False
    else:
        return True


def _check_user_team(user):
    if len(user.yahooteam_set.all()) == 0:
        return False
    else:
        return True
