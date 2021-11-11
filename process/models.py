from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ('can_view_all', 'Can view all'),
        )
    name = models.CharField(verbose_name='申请人', max_length=8, blank=False, null=False)
    cities = models.CharField(verbose_name='所属项目', max_length=16, blank=False, null=False)
    _type = models.CharField(verbose_name='需求类型', max_length=16, blank=False, null=False)
    description = models.CharField(verbose_name='需求描述', max_length=256, blank=False, null=False)
    result = models.CharField(verbose_name='处理结果', max_length=256, blank=False, null=False)
    status = models.CharField(verbose_name='状态', max_length=8, blank=False, null=False, default='进行中')
    processor = models.CharField(verbose_name='处理人', max_length=8, blank=True, null=True, default='')
    create_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    finish_time = models.DateTimeField(verbose_name='完成时间', blank=True, null=True)
    telephone = models.CharField(verbose_name='电话', max_length=15, blank=False, null=False)