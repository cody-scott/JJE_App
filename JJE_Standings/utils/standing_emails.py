from django.core.mail import send_mail
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User

from JJE_Waivers.models import YahooTeam
from JJE_Standings.models import YahooStanding

def send_standings_email(standings_html):
    standings_non_html = "\n".join(
        ["\t".join(
            [str(item[2]), str(item[1]), str(item[3])]) for item in standings_html]
    )
    standings_html = render_to_string("JJE_Standings/email_template.html", {"DATA": standings_html, "DATETIME": timezone.now()})
    week = YahooStanding.objects.filter(current_standings=True).first().standings_week
    subject = "JJE Standings - Week {}".format(week)
    construct_send_email(subject, standings_non_html, standings_html)
    return standings_html


def construct_send_email(subject, body_non_html, body):
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
