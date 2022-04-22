from django.contrib import admin
from django.http import JsonResponse, HttpResponse
from simpleui.admin import AjaxAdmin
import threading
import getlinksapp.function as function
from .models import mission, linksData, domainTable, CaseFile
from import_export.admin import ExportMixin
from import_export import resources
from import_export.fields import Field

# Register your models here.
admin.site.site_title = '暗链扫描系统'
admin.site.site_header = '暗链扫描系统'

# 定义导出的数据源
class linkResource(resources.ModelResource):
    num = Field(attribute='num', column_name='编号')
    link = Field(attribute='link', column_name='链接')
    response_code = Field(attribute='response_code', column_name='响应状态码')
    from_link = Field(attribute='from_link', column_name='源页面')
    abnormal_point = Field(attribute='abnormal_point', column_name='检测到关键词')
    find_time = Field(attribute='find_time', column_name='发现时间')
    class Meta:
        model = linksData
        # exclude = ['mission', 'abnormal']
        exclude = ['mission']

class linkDataAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = linkResource
    list_display = (
        'mission', 'link', 'response_code', 'from_link', 'abnormal_point', 'find_time',)
    list_editable = ()
    readonly_fields = ('num',)
    search_fields = ('link', 'response_code', 'abnormal_point',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (
        ('采集信息', {'fields': (
            'domain', 'link',)}),
        ('响应状态', {'fields': ('response_code',)}),
        # ('异常信息', {'fields': ('abnormal', 'abnormal_point',)}),
        ('异常信息', {'fields': ('abnormal_point',)}),
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
    fieldsets = (('域名信息', {'fields': ('domain',)}),)


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
    actions = ('layer_input', 'upload_file',)

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
    layer_input.confirm = '任务开始成功,或点击取消结束任务！'

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload = request.FILES['upload']
        print('接收到上传的文件', upload.name)
        file = CaseFile()
        file.file_name = upload
        file.save()
        # 开始导入文件
        imp = function.ExcelImport(file_name=file.file_name)
        recode = imp.get_cases()
        if recode == 1:
            return JsonResponse(data={
                'status': 'success',
                'msg': '处理成功！'
            })
        else:
            return JsonResponse(data={
                'status': 'error',
                'msg': str(recode)
            })

    upload_file.short_description = '批量导入'
    upload_file.type = 'success'
    upload_file.icon = 'el-icon-upload'
    upload_file.enable = True

    upload_file.layer = {
        'params': [{
            'type': 'file',
            'tips': '模板在“关于系统“里下载',
            'key': 'upload',
            'label': '请选择xlsx文件'
        }]
    }


admin.site.register(mission, missionAdmin)
