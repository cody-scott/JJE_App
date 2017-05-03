from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from JJE_Waivers.models import WaiverClaim, YahooTeam

import datetime


def create_test_team(team_name):
    new_team = YahooTeam()
    new_team.team_name = team_name
    new_team.save()
    return new_team


def create_claim(add_player, drop_player, team):
    claim = WaiverClaim()
    claim.add_player = add_player
    claim.add_C = True
    claim.drop_player = drop_player
    claim.drop_C = True
    claim.team = team
    claim.save()
    return claim


class WaiverClaimTest(TestCase):
    def test_claim_active(self):
        claim = WaiverClaim()
        self.assertIs(claim.active_claim(), True)

    def test_old_claim_inactive(self):
        claim = WaiverClaim()
        old_time = timezone.now() - datetime.timedelta(days=2)
        claim.claim_start = old_time
        self.assertIs(claim.active_claim(), False)

    def test_cancel_claim(self):
        claim = WaiverClaim()
        claim.cancelled = True
        self.assertIs(claim.active_claim(), False)

    def test_overclaim(self):
        claim = WaiverClaim()
        claim.overclaimed = True
        self.assertIs(claim.active_claim(), False)

    def test_add_position(self):
        claim = WaiverClaim()
        claim.add_C = True
        claim.add_D = True
        self.assertEqual(claim.get_position_add, 'C/D')

    def test_drop_position(self):
        claim = WaiverClaim()
        claim.drop_IR = True
        self.assertEqual(claim.get_position_drop, 'IR')

    def test_claim_end(self):
        claim = WaiverClaim()
        st = timezone.now()
        et = (timezone.now() + datetime.timedelta(days=1)).isoformat()
        claim.claim_start = st
        self.assertEqual(claim.claim_end, et)


class IndexViewTest(TestCase):
    def test_index_no_claim(self):
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(response.context['waiverclaim_list'], [])

    def test_index_one_claim(self):
        st = (timezone.now() - datetime.timedelta(hours=5))
        team = create_test_team("Test")
        claim = create_claim("Test Player Add", "Test Player Drop", team)
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(response.context['waiverclaim_list'], ["<WaiverClaim: Test Player Add>"])

    def test_index_two_claims(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        claim_two = create_claim("Test A P 2", "Test D P 2", team)
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(response.context['waiverclaim_list'],
                                 ["<WaiverClaim: Test A P 1>", "<WaiverClaim: Test A P 2>"], ordered=False)

    def test_old_and_new_claims(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        claim_two = create_claim("Test A P 2", "Test D P 2", team)
        claim_one.claim_start = (timezone.now() - datetime.timedelta(days=2))
        claim_one.save()
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(response.context['waiverclaim_list'],["<WaiverClaim: Test A P 2>"], ordered=False)


class OverclaimViewTest(TestCase):
    def test_null_overclaim(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        response = self.client.get('/waiver_claim/overclaim={}'.format(10))
        self.assertEqual(response.status_code, 302)

    def test_valid_overclaim(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        response = self.client.get('/waiver_claim/overclaim={}'.format(1))
        self.assertEqual(response.status_code, 200)

    def test_overclaim_content(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        response = self.client.get('/waiver_claim/overclaim={}'.format(1))
        self.assertEqual(response.context['add_name'], claim_one.add_player)

    def test_overclaim_submit(self):
        team = create_test_team("Test Team")
        team_two = create_test_team("Team Two")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)

        response = self.client.post('/waiver_claim/overclaim={}'.format(1),
                                    {
                                        'team': team_two.id, 'drop_player': "Drop Test"}
                                    )
        claim_two = WaiverClaim.objects.get(id=2)
        self.assertEqual(claim_two.team.id, team_two.id)

        claim_one = WaiverClaim.objects.get(id=1)
        self.assertIs(claim_one.overclaimed, True)

        self.assertEqual(claim_two.over_claim_id, claim_one.id)


class NewClaimTest(TestCase):
    def test_new_claim(self):
        team = create_test_team("Test Team")
        response = self.client.post('/waiver_claim/new/',
                                    {
                                        'team': team.id,
                                        'add_player': "Test A",
                                        'add_C': True,
                                        'drop_player': "Test D",
                                    }, follow=True)
        response_index = self.client.get(reverse('index'))
        claim_one = WaiverClaim.objects.get(id=1)
        self.assertEqual(claim_one.team.id, team.id)
        self.assertEqual(claim_one.add_player, "Test A")
        self.assertEqual(claim_one.drop_player, "Test D")
        self.assertQuerysetEqual(
            response_index.context["waiverclaim_list"],
            ["<WaiverClaim: Test A>"]
        )

    def test_null_submission_team(self):
        team = create_test_team("Team")
        response = self.client.post('/waiver_claim/new/',
                                    {
                                        'add_player': "Test A",
                                        'add_C': True,
                                        'drop_player': "Test D",
                                    }, follow=True)
        self.assertEqual(response.redirect_chain, [])

    def test_null_submission_add_player(self):
        team = create_test_team("Team")
        response = self.client.post('/waiver_claim/new/',
                                    {
                                        'team': team.id,
                                        'add_player': "Test A",
                                        'add_C': True,
                                        # 'drop_player': "Test D",
                                    }, follow=True)
        self.assertEqual(response.redirect_chain, [])

    def test_null_submission_drop_player(self):
        team = create_test_team("Team")
        response = self.client.post('/waiver_claim/new/',
                                    {
                                        'team': team.id,
                                        # 'add_player': "Test A",
                                        'add_C': True,
                                        'drop_player': "Test D",
                                    }, follow=True)
        self.assertEqual(response.redirect_chain, [])


class CancelClaimTest(TestCase):
    def test_valid_cancel(self):
        team = create_test_team("Test Team")
        claim_one = create_claim("Test A P 1", "Test D P 1", team)
        response = self.client.post('/waiver_claim/cancel={}'.format(claim_one.id))
        claim_one_test = WaiverClaim.objects.get(id=1)
        self.assertIs(claim_one_test.cancelled, True)
