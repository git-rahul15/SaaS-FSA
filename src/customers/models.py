from django.db import models
from django.conf import settings
from helpers import billing
from allauth.account.signals import (user_signed_up as allauth_user_signedup,
                                     email_confirmed as user_email_confirmed)

# Create your models here.


User = settings.AUTH_USER_MODEL  #auth_user
class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    init_email = models.EmailField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            if self.email_confirmed and self.init_email:
                email = self.init_email
                name = self.user.first_name
                if email !="" or email is not None:
                    self.stripe_id = billing.create_customer(name=name,email=email, metadata={'user_id':self.user.id, "username" :self.user.username}, raw=False)
        super().save(*args, **kwargs)

    
def allauth_user_signedup_helper(request, user, *args, **kwargs):
    email = user.email
    Customers.objects.create(
        user = user,
        init_email = email,
        email_confirmed = False,
    )
    

def user_email_confirmed_helper(request, email_address, *args, **kwargs):
    qs = Customers.objects.filter(
        init_email = email_address,
        email_confirmed = False,
    )
    for obj in qs:
        obj.email_confirmed = True
        obj.save()#sends signal
allauth_user_signedup.connect(allauth_user_signedup_helper)


user_email_confirmed.connect(user_email_confirmed_helper)