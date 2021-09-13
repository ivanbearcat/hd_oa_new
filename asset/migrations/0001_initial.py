# Generated by Django 3.2.7 on 2021-09-03 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='x', max_length=64, null=True, verbose_name='资产名称')),
                ('server_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='主机IP')),
                ('ssh_port', models.IntegerField(blank=True, null=True, verbose_name='ssh端口')),
                ('user', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=32, null=True, verbose_name='密码')),
                ('model', models.CharField(blank=True, max_length=32, null=True, verbose_name='型号')),
                ('sn_mainboard', models.CharField(blank=True, max_length=16, null=True, verbose_name='主板序列号')),
                ('sn_BIOS', models.CharField(blank=True, max_length=16, null=True, verbose_name='BIOS序列号')),
                ('cpu', models.CharField(blank=True, max_length=16, null=True, verbose_name='cpu')),
                ('memory', models.CharField(blank=True, max_length=16, null=True, verbose_name='内存')),
                ('disk', models.CharField(blank=True, max_length=16, null=True, verbose_name='硬盘')),
                ('os', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统')),
                ('deployment_plan', models.CharField(blank=True, max_length=32, null=True, verbose_name='部署规划')),
                ('doployment_mod', models.CharField(blank=True, max_length=256, null=True, verbose_name='部署模块')),
                ('remote_card_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='远控卡IP')),
                ('remote_card_user', models.CharField(blank=True, max_length=32, null=True, verbose_name='远控卡用户名')),
                ('remote_card_password', models.CharField(blank=True, max_length=32, null=True, verbose_name='远控卡密码')),
                ('organization', models.CharField(blank=True, max_length=32, null=True, verbose_name='组织实体')),
                ('old_asset_number', models.CharField(blank=True, max_length=32, null=True, verbose_name='旧资产编号')),
                ('new_asset_number', models.CharField(blank=True, default='', max_length=32, null=True, unique=True, verbose_name='新资产编号')),
                ('owner', models.CharField(blank=True, max_length=16, null=True, verbose_name='使用人')),
                ('owner_department', models.CharField(blank=True, max_length=16, null=True, verbose_name='使用部门')),
                ('is_use', models.CharField(blank=True, max_length=16, null=True, verbose_name='使用情况')),
                ('cost_center', models.CharField(blank=True, max_length=16, null=True, verbose_name='成本中心')),
                ('checker', models.CharField(blank=True, max_length=16, null=True, verbose_name='盘点人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='登记时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('_type', models.CharField(blank=True, choices=[('物理机', '物理机'), ('虚拟机', '虚拟机'), ('交换机', '交换机'), ('防火墙', '防火墙'), ('存储设备', '存储设备')], max_length=16, null=True, verbose_name='资产类别')),
                ('location', models.CharField(blank=True, max_length=32, null=True, verbose_name='位置')),
                ('status', models.CharField(choices=[('库存', '库存'), ('出库', '出库'), ('报废', '报废'), ('损坏', '损坏'), ('出库审批', '出库审批'), ('报废审批', '报废审批')], default='库存', max_length=16, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '资产表',
                'permissions': (('can_view_password', 'Can view password'), ('approver', 'approver')),
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(max_length=1024, verbose_name='备注')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.table')),
            ],
        ),
    ]
