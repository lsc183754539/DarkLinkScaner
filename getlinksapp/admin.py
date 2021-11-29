from django.contrib import admin
from django.forms import model_to_dict
from django.http import JsonResponse
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from simpleui.admin import AjaxAdmin

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


# admin.site.register(domainTable, domainTableAdmin)


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
    list_per_page = 50
    # 增加自定义按钮
    actions = ['custom_button']

    def custom_button(self, request, queryset):
        for queryset_item in queryset:
            requests.post('http://127.0.0.1:8000/start', verify=False, data=model_to_dict(queryset_item))

    # 显示的文本，与django admin一致
    custom_button.short_description = '开始扫描任务'
    # icon，参考element-ui icon与https://fontawesome.com
    custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'primary'

    # 给按钮追加自定义的颜色
    custom_button.style = 'color:white;'


admin.site.register(mission, missionAdmin)


# 测试Admin
class RecordAdmin(ImportExportActionModelAdmin, AjaxAdmin):
    resource_class = resources
    list_display = (
        'domain',)
    list_editable = ()
    readonly_fields = ()
    search_fields = ('domain',)
    empty_value_display = 'N/A'
    list_filter = ()
    fieldsets = (('域信息', {'fields': ('domain',)}),)
    list_per_page = 10

    actions = ('layer_input',)

    def layer_input(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            print('tttt')
            return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })
        else:
            print('ttad')
            return JsonResponse(data={
                'status': 'success',
                'msg': '处理成功！'
            })

    layer_input.short_description = '弹出对话框输入'
    layer_input.type = 'success'
    layer_input.icon = 'el-icon-s-promotion'

    # 指定一个输入参数，应该是一个数组

    # 指定为弹出层，这个参数最关键
    layer_input.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '弹出层输入框',
        # 提示信息
        'tips': '这个弹出对话框是需要在admin中进行定义，数据新增编辑等功能，需要自己来实现。',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [{
            # 这里的type 对应el-input的原生input属性，默认为input
            'type': 'input',
            # key 对应post参数中的key
            'key': 'name',
            # 显示的文本
            'label': '名称',
            # 为空校验，默认为False
            'require': True
        }, {
            'type': 'select',
            'key': 'type',
            'label': '类型',
            'width': '200px',
            # size对应elementui的size，取值为：medium / small / mini
            'size': 'small',
            # value字段可以指定默认值
            'value': '0',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }]
        }, {
            'type': 'number',
            'key': 'money',
            'label': '金额',
            # 设置默认值
            'value': 1000
        }, {
            'type': 'date',
            'key': 'date',
            'label': '日期',
        }, {
            'type': 'datetime',
            'key': 'datetime',
            'label': '时间',
        }, {
            'type': 'rate',
            'key': 'star',
            'label': '评价等级'
        }, {
            'type': 'color',
            'key': 'color',
            'label': '颜色'
        }, {
            'type': 'slider',
            'key': 'slider',
            'label': '滑块'
        }, {
            'type': 'switch',
            'key': 'switch',
            'label': 'switch开关'
        }, {
            'type': 'input_number',
            'key': 'input_number',
            'label': 'input number'
        }, {
            'type': 'checkbox',
            'key': 'checkbox',
            # 必须指定默认值
            'value': [],
            'label': '复选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }, {
            'type': 'radio',
            'key': 'radio',
            'label': '单选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }]
    }


admin.site.register(domainTable, RecordAdmin)
