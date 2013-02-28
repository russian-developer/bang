# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from social_auth.db.django_models import UserSocialAuth

class FuckIt(models.Model):

    me = models.CharField(max_length=255)
    fuckit = models.CharField(max_length=255)
    send = models. BooleanField(default=True)

    def __unicode__(self):
        return '{0} -> {1}'.format(self.me, self.fuckit)


def send_post_wall(sender, instance, created, **kwargs):
    if (created and sender.__name__ == 'UserSocialAuth'):
        pass

def send_messages(sender, instance, created, **kwargs):
    if (created and sender.__name__ == 'FuckIt'):
        me = instance.me
        fuckit = instance.fuckit
        if sender.objects.filter(fuckit=me, me=fuckit, send=False).exists():
            # Send message to...
            f = sender.objects.get(fuckit=me, me=fuckit, send=False)
            f.send = True
            f.save()

post_save.connect(send_post_wall, sender=UserSocialAuth)
post_save.connect(send_messages, sender=FuckIt)