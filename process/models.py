from django.db import models

class table(models.Model):
    name = models.CharField(verbose_name='申请人', max_length=8, blank=False, null=False)
    cities = models.CharField(verbose_name='所属项目', max_length=16, blank=False, null=False)
    _type = models.CharField(verbose_name='需求类型', max_length=16, blank=False, null=False)
    description = models.CharField(verbose_name='需求描述', max_length=256, blank=False, null=False)
    status = models.CharField(verbose_name='状态', max_length=8, blank=False, null=False, default='进行中')
    processor = models.CharField(verbose_name='处理人', max_length=8, blank=True, null=True, default='')
    create_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)