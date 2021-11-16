from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class linksData(models.Model):
    num = models.AutoField(primary_key=True, verbose_name="编号", )
    mission = models.ForeignKey('domainTable', related_name='domainTable1', on_delete=models.CASCADE, verbose_name='域',
                               null=True, blank=True, )
    link = models.TextField(verbose_name="链接", null=True, blank=True, )
    from_link = models.TextField(verbose_name='发现页面', null=True, blank=True, )
    response_code = models.IntegerField(verbose_name='响应状态码', null=True, blank=True, )
    abnormal = models.BooleanField(verbose_name='是否异常', null=True, blank=True, )
    abnormal_point = models.TextField(verbose_name='异常点', null=True, blank=True, )
    find_time = models.DateTimeField(verbose_name='发现时间', null=True, blank=True, )

    def __str__(self):
        return str(self.num)

    class Meta:
        verbose_name = "链接信息"
        verbose_name_plural = "链接库"


class mission(models.Model):
    num = models.AutoField(primary_key=True, verbose_name="编号")
    url = models.TextField(verbose_name="入口链接", null=True, blank=True, )
    domain = models.ForeignKey('domainTable', related_name='domainTable', on_delete=models.CASCADE, verbose_name='域',
                               null=True, blank=True, )

    def __str__(self):
        return str(self.num)

    class Meta:
        verbose_name = "任务信息"
        verbose_name_plural = "任务库"


class domainTable(models.Model):
    domain = models.TextField(verbose_name='域', null=True, blank=True, )

    def __str__(self):
        return str(self.domain)

    class Meta:
        verbose_name = "域信息"
        verbose_name_plural = "域库"
