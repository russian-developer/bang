# -*- coding: utf-8 -*-

import httplib2
import json

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from social_auth.db.django_models import UserSocialAuth
from settings import *
from libs.render import render_to
from models import FuckIt

class Wrap(object):

    def __init__(self, user):
        self.user = user
        self.us = UserSocialAuth.objects.get(user=user)

    def profile(self):
        return {}

    def friends(self):
        return []


class VK(Wrap):

    vk = 'https://api.vk.com/method/'

    def profile(self):
        url = '{0}getProfiles.json?fields=uid,first_name,last_name,sex&uid={1}&access_token={2}'.format(self.vk, self.us.uid, self.us.extra_data['access_token'])
        http = httplib2.Http()
        response = http.request(url)
        status = response[0]
        if status['status'] == '200':
            try:
                j = json.loads(str(response[1]))
                prof = j['response'][0]
            except:
                pass
        return prof

    def friends(self):
        users = []
        url = '{0}getFriends.json?fields=uid,first_name,last_name,nickname,sex,photo_big&uid={1}&access_token={2}'.format(self.vk, self.us.uid, self.us.extra_data['access_token'])
        http = httplib2.Http()
        response = http.request(url)
        status = response[0]
        if status['status'] == '200':
            try:
                j = json.loads(str(response[1]))
                users = j['response']
            except:
                pass
        return users


class Social(Wrap):

    def profile(self):
        w = Wrap(self.user)
        if self.us.provider == 'vkontakte-oauth2':
            w = VK(self.user)
        return w.profile()

    def friends(self):
        w = Wrap(self.user)
        if self.us.provider == 'vkontakte-oauth2':
            w = VK(self.user)
        return w.friends()


@render_to('fuck.html')
def fuck(request):
    user = request.user
    if (user.is_authenticated() and user.is_active):
        s = Social(user)
        prof = s.profile()
        if len(prof) == 0:
            return HttpResponseRedirect('/')
        try:
            sex = int(request.GET.get('sex', prof['sex']))
        except:
            sex = int(prof['sex'])
        if  sex not in [1, 2]:
            sex = int(prof['sex'])
        if sex == 1:
            sex = 2
        elif sex == 2:
            sex = 1
        friends = []
        for f in s.friends():
            if int(f['sex']) == sex:
                friends.append({
                    'fuck': FuckIt.objects.filter(me=prof['uid'], fuckit=f['uid']).exists(),
                    'first_name': f['first_name'], 
                    'last_name': f['last_name'],
                    'photo_big': f['photo_big'],
                    'sex': f['sex'],
                    'uid': f['uid'],
                })
        return {
            'prof': prof,
            'sex': sex,
            'friends': friends,
        }
    else:
        return HttpResponseRedirect('/')

def fuckit(request, uid):
    user = request.user
    if (user.is_authenticated() and user.is_active):
        s = Social(user)
        prof = s.profile()
        if len(prof) == 0:
            return HttpResponseRedirect('/')
        friends = s.friends()
        for f in friends:
            if f['uid'] == uid:
                if not FuckIt.objects.filter(me=prof['uid'], fuckit=uid).exists():
                    fk = FuckIt.objects.create(
                        me = prof['uid'],
                        fuckit = uid
                    )
                    break
    return HttpResponseRedirect(reverse('app.views.fuck'))

@render_to('index.html')
def index(request):
    return {}
