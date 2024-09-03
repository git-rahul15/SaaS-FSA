from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from helpers import billing
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL #auth.user


ALLOWED_CUSTOM_GROUPS = True
SUBSCRIPTIONS_PERMISSIONS = [
            ("basic", "Basic Permissions"),
            ("pro", "Pro Permissions"),
            ("advance", "Advanced Permissions"),
            ("basic plus", 'Basic Plus Permissions')

        ]


class Subscriptions(models.Model):


    """
    Subscriptions  = Stripe Product
    """


    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={'content_type__app_label':'subscription', 'codename__in':[x[0] for x in SUBSCRIPTIONS_PERMISSIONS]}) #limit_choices_to={'content_type__app_label':'subscriptions'} to limit permission of just about this subscriptions model in admin panel
    product_id = models.CharField(max_length=120, null=True, blank=True)
    plan_description = models.TextField(max_length=500, null=True)
    order = models.IntegerField(default=-1)
    featured = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text="Features of plan, seperaterd by new line", blank=True, null=True)


    def get_features_as_list(self):
        if not self.features:
            return []
        return [feature.strip() for feature in  self.features.split('\n')]


    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = billing.create_product(name=self.name, metadata={"subscriptions_id":self.id},active=self.active, raw=False, description=self.plan_description)
        super().save(*args, **kwargs)

    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSIONS
        ordering = ["order", "featured", "-updated"]

    

    #subscriptions.pro
    #subscriptions.basic
    #subscriptions.advance


class SubscriptionPrice(models.Model):
    
    """
    Subscription Price = Stipe Price
    
    """
    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"

    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    product_price_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places= 0,default=349)
    order = models.IntegerField(default=-1)
    featured = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["subscription__order", "order", "featured", "-updated"]

    def get_checkout_url(self):
        return reverse("sub-price-checkout", kwargs={"price_id":self.product_price_id})

    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()
    

    @property
    def stripe_currency(self):
        return 'INR'
    
    @property
    def stripe_price(self):
       return self.price * 100 #return an integer price as its reuiqred for stripe
    
    @property
    def product_id(self):
        if not self.subscription:
            return None
        return self.subscription.product_id
    
    def save(self, *args, **kwargs):
        if (not self.product_price_id and self.product_id is not None ):
            product_price_id = billing.create_product_price(currency=self.stripe_currency, unit_amount=self.stripe_price,interval=self.interval, product=self.product_id, metadata={"subscription_plan_price_id":self.id}, raw=False)


            self.product_price_id = product_price_id
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription = self.subscription,
                interval = self.interval).exclude(id=self.id)
            qs.update(featured = False)
    


class UserSubscriptions(models.Model):
    def __str__(self):
        return self.user.username
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_post_sub_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    subscription_obj = user_sub_instance.subscriptions
    groups_ids =[]
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat = True)    
    user = user_sub_instance.user
    if not ALLOWED_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscriptions.objects.filter(active = True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id = subscription_obj.id)
        subs_groups = subs_qs.values_list('groups__id', flat=True)
        subs_groups_set = set(subs_groups)

        # groups_ids = groups.values_list('id', flat = True) #gives the list of groups name id
        current_groups_ids = user.groups.all().values_list('id', flat = True)
        groups_ids_sets = set(groups_ids)
        current_groups_ids_sets = set(current_groups_ids) - subs_groups_set
        final_groups_ids = list(groups_ids_sets | current_groups_ids_sets)
        user.groups.set(final_groups_ids)
        # print(final_groups_ids)


post_save.connect(user_post_sub_save, sender=UserSubscriptions)