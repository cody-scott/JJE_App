from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse

from JJE_Waivers.models import WaiverClaim, YahooTeam
from JJE_Standings.models import YahooStanding

from django.utils import timezone
from datetime import timedelta

from JJE_Waivers.utils import email_functions

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


class IndexView(ListView):
    template_name = "JJE_Waivers/waivers_index.html"

    def get_queryset(self):
        now = timezone.now() - timedelta(days=1)
        claims = WaiverClaim.objects.filter(cancelled=False).filter(overclaimed=False).filter(claim_start__gt=now) \
            .order_by('claim_start')
        return claims

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # user_teams = [team_id.id for team_id in YahooTeam.objects.all()]
        user_teams = []
        overclaim_teams = []
        if not self.request.user.is_anonymous:
            teams = self.request.user.yahooteam_set.all()
            user_teams = [team_id.id for team_id in teams]
            overclaim_teams = get_current_ranks(self.request.user)

        context['user_team_ids'] = user_teams
        context['overclaim_ids'] = overclaim_teams
        return context


@method_decorator(login_required, name='dispatch')
class WaiverClaimCreate(CreateView):
    model = WaiverClaim
    template_name_suffix = "_new"
    fields = [
        "team",
        "add_player", "add_LW", "add_C", "add_RW", "add_D", "add_G", "add_Util", "add_IR",
        "drop_player", "drop_LW", "drop_C", "drop_RW", "drop_D", "drop_G", "drop_Util", "drop_IR"
    ]

    def get_form(self, form_class=None):
        frm = super(WaiverClaimCreate, self).get_form(form_class)
        frm.fields['team'].queryset = YahooTeam.objects.filter(user=self.request.user.id)
        return frm

    def get_initial(self):
        return get_user_teams_list(self.request.user)

    def form_valid(self, form):
        valid_form = super(WaiverClaimCreate, self).form_valid(form)
        email_functions.new_claim_email(self.object)
        return valid_form


@method_decorator(login_required, name='dispatch')
class OverclaimCreate(CreateView):
    model = WaiverClaim
    template_name_suffix = "_overclaim"
    fields = [
        "team",
        "drop_player", "drop_LW", "drop_C", "drop_RW", "drop_D", "drop_G", "drop_Util", "drop_IR"
    ]

    def get(self, request, *args, **kwargs):
        try:
            wc_id = self.kwargs.get("waiver_claim_id")
            player = WaiverClaim.objects.get(id=wc_id)
            assert player.active_claim()

            claim_team_standing = get_claim_rank(player.team)
            claimee_standings = []
            for item in self.request.user.yahooteam_set.all():
                claimee_standings.extend([z.rank for z in item.yahoostanding_set.filter(current_standings=True).all()])

            if len(claim_team_standing) > 0 and len(claimee_standings) > 0:
                cts = max(claim_team_standing)
                cee = max(claimee_standings)
                if cts > cee:
                    raise AssertionError

            return super(OverclaimCreate, self).get(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect(reverse("index"))

    def get_initial(self):
        return get_user_teams_list(self.request.user)

    def get_form(self, form_class=None):
        frm = super(OverclaimCreate, self).get_form(form_class)
        wc_id = self.kwargs.get("waiver_claim_id")
        player = WaiverClaim.objects.get(id=wc_id)
        frm.fields['team'].queryset = self.get_rank(self.request, player)
        return frm

    def get_context_data(self, **kwargs):
        context = super(OverclaimCreate, self).get_context_data(**kwargs)
        wc_id = self.kwargs.get("waiver_claim_id")
        player = WaiverClaim.objects.get(id=wc_id)
        context["add_name"] = player.add_player
        context["add_pos"] = player.get_position_add
        return context

    def form_valid(self, form):
        wc_id = self.kwargs.get("waiver_claim_id")
        player = WaiverClaim.objects.get(id=wc_id)
        player.overclaimed = True
        player.save()

        form.instance.claim_start = player.claim_start
        form.instance.add_player = player.add_player
        form.instance.add_LW = player.add_LW
        form.instance.add_C = player.add_C
        form.instance.add_RW = player.add_RW
        form.instance.add_D = player.add_D
        form.instance.add_G = player.add_G
        form.instance.add_Util = player.add_Util
        form.instance.add_IR = player.add_IR
        form.instance.over_claim_id = int(wc_id)
        valid_form = super(OverclaimCreate, self).form_valid(form)

        email_functions.overclaim_email(self.object)

        return valid_form

    def get_rank(self, request, player):
        try:
            player = player #type: WaiverClaim
            rank = player.team.yahoostanding_set.filter(current_standings=True).first().rank
            ranks = [team.team.id for team in YahooStanding.objects.filter(current_standings=True)
                .filter(rank__gte=rank).all()]
            return YahooTeam.objects.filter(pk__in=ranks).filter(user=self.request.user.id)
        except:
            return YahooTeam.objects.filter(user=self.request.user.id).exclude(id=player.team.id)


@method_decorator(login_required, name='dispatch')
class CancelClaimView(DetailView):
    template_name = 'JJE_Waivers/waiverclaim_cancel.html'
    model = WaiverClaim

    def get(self, request, *a, **k):
        id = int(k.get("pk"))
        claim_obj = WaiverClaim.objects.filter(id=id).first() #type: WaiverClaim
        if claim_obj is None or not claim_obj.active_claim():
            return redirect(reverse("index"))

        if self.check_if_user_claim(request, id):
            return super(CancelClaimView, self).get(request, *a, **k)
        else:
            return redirect(reverse("index"))

    def check_if_user_claim(self, request, id):
        for team in [team for team in self.request.user.yahooteam_set.all()]:
            claims = [claim.id for claim in team.waiverclaim_set.all()]
            if id in claims:
                return True
        return False

    def post(self, request, *args, **kwargs):
        claim_id = kwargs.get("pk")
        claim = get_object_or_404(WaiverClaim, id=claim_id)
        claim.cancelled = True
        claim.save()
        email_functions.cancel_email(claim)
        return redirect(reverse('index'))
