from django.contrib import admin
from django.http import JsonResponse, HttpResponse
from simpleui.admin import AjaxAdmin
import threading
import getlinksapp.function as function
from .models import mission, linksData, domainTable

# Register your models here.
admin.site.site_title = '暗链扫描系统'
admin.site.site_header = '暗链扫描系统'


class linkDataAdmin(admin.ModelAdmin):
    list_display = (
        'mission', 'link', 'response_code', 'from_link', 'abnormal', 'abnormal_point', 'find_time',)
    list_editable = ()
    readonly_fields = ('num',)
    search_fields = ('mission__domain', 'link', 'response_code', 'abnormal', 'abnormal_point',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (
        ('采集信息', {'fields': (
            'domain', 'link',)}),
        ('响应状态', {'fields': ('response_code',)}),
        ('异常信息', {'fields': ('abnormal', 'abnormal_point',)}),
    )


admin.site.register(linksData, linkDataAdmin)


class domainTableAdmin(admin.ModelAdmin):
    list_display = (
        'domain',)
    list_editable = ()
    readonly_fields = ()
    search_fields = ('domain',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (('域信息', {'fields': ('domain',)}),)


admin.site.register(domainTable, domainTableAdmin)


class missionAdmin(AjaxAdmin):
    list_display = ('url', 'domain',)
    list_editable = ()
    readonly_fields = ('num',)
    search_fields = ('url', 'domain',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (('任务信息', {'fields': ('url', 'domain',)}),)
    list_per_page = 50

    # 增加自定义按钮
    actions = ('layer_input',)

    def layer_input(self, request, queryset):
        # 接收到的queryset即为选中的数据的model数据组成的列表
        for mission in queryset:
            mission_url = mission.url
            mission_domain = mission.domain
            t = threading.Thread(target=function.getLinks,
                                 kwargs={'url': mission_url, 'domain': mission_domain},
                                 name='扫描任务：' + str(mission_domain))
            t.setDaemon(False)
            t.start()
            print('[√] ', str(mission_domain) + ' had run!\n')
        return HttpResponse(status=302, headers={'location': '/getlinksapp/linksdata/'})

    layer_input.short_description = '开始扫描选中任务'
    layer_input.type = 'primary'
    layer_input.icon = 'el-icon-s-promotion'
    # 指定为弹出层，这个参数最关键
    # layer_input.layer = {
    #     # 弹出层中的输入框配置
    #     'title': '任务提示',
    #     'tips': '任务已经开始，结果请在链接库中查看！',
    #     'confirm_button': '明白',
    #     'width': '50%',
    # }
    layer_input.confirm = '任务开始成功,或点击取消结束任务！'


admin.site.register(mission, missionAdmin)
