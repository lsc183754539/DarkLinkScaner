from django.contrib import admin
from .models import mission, linksData, domainTable
import requests

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


class missionAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'domain',)
    list_editable = ()
    readonly_fields = ('num',)
    search_fields = ('url', 'domain',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (
        ('任务信息', {'fields': (
            'url', 'domain',)}),)
    # 增加自定义按钮
    actions = ['custom_button']

    def custom_button(self, request, queryset):
        requests.get('http://127.0.0.1:8000/start', verify=False)   # 这个地方要改
        pass

    # 显示的文本，与django admin一致
    custom_button.short_description = '开始扫描任务'
    # icon，参考element-ui icon与https://fontawesome.com
    custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'primary'

    # 给按钮追加自定义的颜色
    custom_button.style = 'color:white;'


admin.site.register(mission, missionAdmin)
