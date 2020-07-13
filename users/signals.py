import datetime as dt

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out

from users.models import LogoutTime, User


@receiver(user_logged_out, sender=User)
def logout_sniffer(sender, user, request, **kwargs):
    if LogoutTime.objects.filter(user=user).exists():
        record = LogoutTime.objects.get(user=user)
        record.logout = dt.datetime.now() - dt.timedelta(hours=3)
        record.save()
    else:
        LogoutTime.objects.create(user=user, logout=dt.datetime.now())