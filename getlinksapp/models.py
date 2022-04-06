from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class linksData(models.Model):
    num = models.AutoField(primary_key=True, verbose_name="编号", )
    mission = models.ForeignKey('domainTable', related_name='domainTable1', on_delete=models.CASCADE, verbose_name='域',
                                null=True, blank=True, )
    link = models.CharField(max_length=9999, default=None, verbose_name="链接", null=True, blank=True, )
    from_link = models.CharField(max_length=9999, default=None, verbose_name='发现页面', null=True, blank=True, )
    response_code = models.IntegerField(verbose_name='响应状态码', null=True, blank=True, )
    # abnormal = models.BooleanField(verbose_name='是否异常', null=True, blank=True, )
    abnormal_point = models.CharField(max_length=9999, default=None, verbose_name='异常点', null=True, blank=True, )
    find_time = models.DateTimeField(verbose_name='发现时间', null=True, blank=True, )

    def __str__(self):
        return str(self.num)

    class Meta:
        verbose_name = "链接信息"
        verbose_name_plural = "扫描结果"


class mission(models.Model):
    num = models.AutoField(primary_key=True, verbose_name="编号")
    url = models.CharField(max_length=100, default='只是作为扫描任务的入口！示例：http://www.tsinghua.edu.cn/index.html',
                           verbose_name="任务开始链接（扫描由此开始）", null=True, blank=True, )
    domain = models.ForeignKey('domainTable', related_name='domainTable', on_delete=models.CASCADE,
                               verbose_name='扫描的域名',
                               null=True, blank=True, )

    def __str__(self):
        return str(self.num)

    class Meta:
        verbose_name = "任务信息"
        verbose_name_plural = "任务库"


class domainTable(models.Model):
    domain = models.CharField(max_length=100, default='只能填一个域名！示例：www.tsinghua.edu.cn', verbose_name='域名',
                              null=True, blank=True, )

    def __str__(self):
        return str(self.domain)

    class Meta:
        verbose_name = "域名信息"
        verbose_name_plural = "域名库"


# 用例文件
class CaseFile(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    file_name = models.FileField(upload_to='xlsfile/%Y/%m/%d/', verbose_name=u"文件名称")

    # 不注释会报错
    # def __str__(self):
    #     return self.file_name

    # 定义表名称
    class Meta:
        verbose_name = "文件管理"
        verbose_name_plural = "文件管理"
