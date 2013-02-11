# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from social_auth.db.django_models import UserSocialAuth

class FuckIt(models.Model):

    me = models.CharField(max_length=255)
    fuckit = models.CharField(max_length=255)

    def __unicode__(self):
        return self.fuckit


def send_post_wall(sender, instance, created, **kwargs):
    if (created and sender.__name__ == 'UserSocialAuth'):
        pass

def send_messages(sender, instance, created, **kwargs):
    if (created and sender.__name__ == 'FuckIt'):
        pass

post_save.connect(send_post_wall, sender=UserSocialAuth)
post_save.connect(send_messages, sender=FuckIt)