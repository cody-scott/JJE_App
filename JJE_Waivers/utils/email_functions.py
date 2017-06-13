from django.core.mail import send_mail
from django.template import Context, Template

from JJE_Waivers.models import YahooTeam, WaiverClaim

from JJE_App.settings import email_super_users, email_admins
from django.contrib.auth.models import User


def overclaim_email(waiver_claim):
    send_waiver_email(waiver_claim, "Overclaim")


def new_claim_email(waiver_claim):
    send_waiver_email(waiver_claim, "New Claim")


def cancel_email(waiver_claim):
    body = "<h1>Cancelled Claim</h1>" \
           "<h1>Team: {}</h1>\n" \
           "<h2>Player: {}</h2>\n" \
           "<h3><a href=\"https://jje-fantasy-app.herokuapp.com\">Claim Site</a></h3>".format(
        waiver_claim.team.team_name,
        waiver_claim.add_player)
    body_non_html = "{}]n{}".format(
        waiver_claim.team.team_name,
        waiver_claim.add_player
    )
    construct_send_email("Cancelled Claim", body_non_html, body)



def send_waiver_email(waiver_object, message_type):
    subject, body, body_non_html = format_waiver_claim(waiver_object, message_type)
    construct_send_email(subject=subject, body=body, body_non_html=body_non_html)


def format_waiver_claim(waiver_object, message_type):
    waiver_object = waiver_object # type: WaiverClaim

    body = "<h1>Claimee: {}</h1>\n" \
           "<h2>Add: {}</h2>\n" \
           "<h2>Drop: {}</h2>\n" \
           "<h2>Claim Start (UTC): {}</h2>\n" \
           "<h2>Claim End (UTC): {}</h2>\n" \
           "<h2><a href=\"\">Overclaim Link</a><h2>\n" \
           "<h3><a href=\"https://jje-fantasy-app.herokuapp.com\">Claim Site</a></h3>".format(
        waiver_object.team.team_name,
        waiver_object.add_player,
        waiver_object.drop_player,
        waiver_object.claim_start,
        waiver_object.claim_end_normal
    )

    body_non_html = "{}\n{}\n{}\n{}\n{}".format(
        waiver_object.team.team_name,
        waiver_object.add_player,
        waiver_object.drop_player,
        waiver_object.claim_start,
        waiver_object.claim_end_normal
    )

    subject = "John Jones - {}".format(message_type)
    return subject, body, body_non_html


def construct_send_email(subject, body_non_html, body):
    if email_super_users:
        emails = superuser_emails()
    elif email_admins:
        emails = admin_emails()
    else:
        emails = get_available_emails()
    send_mail(subject=subject, message=body_non_html, from_email="jje.waivers@gmail.com",
              html_message=body, recipient_list=emails)


def get_available_emails():
    teams = YahooTeam.objects.all()
    emails = []

    for team in teams:
        if team.user is not None:
            emails.append(team.user.email)
        else:
            emails.append(team.manager_email)

    return [email for email in emails if email != ""]


def superuser_emails():
    users = User.objects.filter(is_superuser=True).all()
    return [user.email for user in users]


def admin_emails():
    users = User.objects.filter(is_staff=True)
    return [user.email for user in users]
