from typing import Any
from django.core.management.base import BaseCommand
from subscription.models import Subscriptions


class Command(BaseCommand):
    def handle(self, *args:Any, **options:Any):
        qs = Subscriptions.objects.filter(active = True)
        #print(qs)
        for obj in qs:
            #print(obj)
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                #print(group)
                group.permissions.set(sub_perms)
                # for per in obj.permission.all():
                #     group.permissions.add(per)

