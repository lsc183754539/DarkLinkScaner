from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from getlinksapp.models import linksData
import getlinksapp.models
import requests
import time
import threading
import getlinksapp.function
# Create your views here.


# 忽略https有效性验证
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def start_scan(request):
    request_mission = request.POST.get('num')
    missions = getlinksapp.models.mission.objects.filter(num__exact=int(request_mission))
    for mission in missions:
        mission_url = mission.url
        mission_domain = mission.domain
        t = threading.Thread(target=getlinksapp.function.getLinks,
                             kwargs={'url': mission_url, 'domain': mission_domain}, name='扫描任务：' + str(mission_domain))
        t.setDaemon(False)
        t.start()
        print('[√] ', str(mission_domain) + ' had run!\n')
    return JsonResponse(data={
        'status': 'success',
        'msg': '任务开始成功！'
    })
