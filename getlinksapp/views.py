from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from getlinksapp.models import linksData
import getlinksapp.models
import requests
import time
import getlinksapp.function
# Create your views here.


# 忽略https有效性验证
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def start_scan(request):
    missions = getlinksapp.models.mission.objects.all()
    for mission in missions:
        mission_url = mission.url
        mission_domain = mission.domain
        getlinksapp.function.getLinks(url=mission_url, domain=mission_domain)
