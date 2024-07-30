from django.db import models
from django.contrib.auth.models import Group, Permission

# Create your models here.

SUBSCRIPTIONS_PERMISSIONS = [
            ("basic", "Basic Permissions"),
            ("pro", "Pro Permissions"),
            ("advance", "Advanced Permissions"),
            ("basic plus", 'Basic Plus Permissions')

        ]


class Subscriptions(models.Model):


    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={'content_type__app_label':'subscription', 'codename__in':[x[0] for x in SUBSCRIPTIONS_PERMISSIONS]}) #limit_choices_to={'content_type__app_label':'subscriptions'} to limit permission of just about this subscriptions model in admin panel


    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSIONS

    #subscriptions.pro
    #subscriptions.basic
    #subscriptions.advance