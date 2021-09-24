from django.contrib import admin
from .models import table, comment
from django.http import HttpResponse, HttpResponseRedirect
from openpyxl import Workbook
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.options import get_content_type_for_model
from django.contrib import messages
from django.utils.html import format_html
from admin_confirm import AdminConfirmMixin
from admin_confirm.admin import confirm_action


class ExportExcelMixin(AdminConfirmMixin, object):
    # 自定义actions导出Excel
    @confirm_action
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        field_verbose_names = [field.verbose_name for field in meta.fields]
        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_verbose_names)
        for obj in queryset:
            for _ in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]
            ws.append(data)
        wb.save(response)
        return response
    export_as_excel.short_description = '导出Excel'



class commentInline(admin.StackedInline):
    extra = 0    # 默认打开创建数量
    model = comment    # 关联外键表



# Register your models here.
@admin.register(table)
class tableAdmin(admin.ModelAdmin, ExportExcelMixin, AdminConfirmMixin):
    inlines = [commentInline]
    # 自定义字段：外键备注
    def commnet(self, obj):
        return [ i.info for i in obj.comment_set.all()]
    commnet.short_description = "备注"

    list_display = ('name', 'status', 'server_ip', 'ssh_port', 'user', 'model', 'sn_mainboard', 'sn_BIOS', 'cpu',
                    'memory', 'disk', 'os', 'deployment_plan','doployment_mod', 'remote_card_ip', 'remote_card_user',
                    'organization', 'old_asset_number', 'new_asset_number', 'owner', 'owner_department', 'is_use',
                    '_type', 'cost_center', 'checker', 'create_time', 'update_time', 'location', 'commnet')

    # list_display_links = ('server_ip',)

    readonly_fields = ('organization', 'location')

    search_fields = ('name', 'server_ip', 'model', 'sn_mainboard', 'sn_BIOS', 'owner', 'checker', 'is_use',
                     'remote_card_ip', 'new_asset_number', 'location')

    date_hierarchy = 'create_time'

    list_per_page = 5

    list_filter = ('status',)

    actions = ['export_as_excel', 'outbound', '_check', 'damage', 'scrap', 'approve']

    # 出库action
    @confirm_action
    def outbound(self, request, queryset):
        for obj in queryset:
            if obj.status == '库存' or obj.status == '使用中':
                obj.status = '出库审批'
                obj.save()
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(obj).pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='出库(需要审批)',
                )
            else:
                messages.add_message(request, messages.ERROR, f'{obj.name} 出库失败，状态错误')

        # self.message_user(request, '执行成功')
    outbound.short_description = '出库'

    # 盘点action
    @confirm_action
    def _check(self, request, queryset):
        for obj in queryset:
            if obj.status == '出库' or obj.status == '库存' or obj.status == '使用中':
                obj.status = '库存'
                obj.checker = request.user.username
                obj.save()
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(obj).pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='盘点',
                )
            else:
                messages.add_message(request, messages.ERROR, f'{obj.name} 盘点失败，状态错误')
        # self.message_user(request, '执行成功')
    _check.short_description = '盘点'

    # 损坏action
    @confirm_action
    def damage(self, request, queryset):
        for obj in queryset:
            if obj.status == '出库' or obj.status == '库存':
                obj.status = '损坏'
                obj.save()
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(obj).pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='设为损坏',
                )
            else:
                messages.add_message(request, messages.ERROR, f'{obj.name} 设置损坏失败，状态错误')
        # self.message_user(request, '执行成功')
    damage.short_description = '损坏'

    # 报废action
    @confirm_action
    def scrap(self, request, queryset):
        for obj in queryset:
            if obj.status == '出库' or obj.status == '库存':
                obj.status = '报废审批'
                obj.save()
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(obj).pk,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=CHANGE,
                    change_message='设为报废(需要审批)',
                )
            else:
                messages.add_message(request, messages.ERROR, f'{obj.name} 设置报废失败，状态错误')
        # self.message_user(request, '执行成功')
    scrap.short_description = '报废'

    # 审批action
    @confirm_action
    def approve(self, request, queryset):
        for obj in queryset:
            if request.user.has_perm('asset.approver') or request.user.is_superuser:
                if '审批' in obj.status:
                    obj.status = obj.status[:-2]
                    obj.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=get_content_type_for_model(obj).pk,
                        object_id=obj.pk,
                        object_repr=str(obj),
                        action_flag=CHANGE,
                        change_message='审批通过',
                    )
                else:
                    messages.add_message(request, messages.ERROR, f'{obj.name} 审批失败，状态错误')
            else:
                messages.add_message(request, messages.ERROR, '没有审批权限')
        # self.message_user(request, '执行成功')
    approve.short_description = '通过审批'

    # 重写函数，增加限制没有查看密码权限的用户不显示密码
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            self.fieldsets = [
                (None, {'fields': ['name', 'server_ip', 'ssh_port', 'user', 'model', 'sn_mainboard', 'sn_BIOS', 'cpu',
                                   'memory', 'disk', 'os', 'deployment_plan', 'doployment_mod', 'remote_card_ip',
                                   'remote_card_user', 'organization', 'old_asset_number', 'new_asset_number', 'owner',
                                   'owner_department', 'is_use', '_type', 'cost_center', 'checker', 'location', 'status']}),
                ('密码', {'fields': ['password', 'remote_card_password'], 'classes': ['collapse']}),
            ]
        elif request.user.has_perm('asset.can_view_password') or request.user.is_superuser:
            self.fieldsets = [
                (None, {'fields': ['name', 'server_ip', 'ssh_port', 'user', 'model', 'sn_mainboard', 'sn_BIOS', 'cpu',
                                   'memory', 'disk', 'os', 'deployment_plan', 'doployment_mod', 'remote_card_ip',
                                   'remote_card_user', 'organization', 'old_asset_number', 'new_asset_number', 'owner',
                                   'owner_department', 'is_use', '_type', 'cost_center', 'checker', 'location']}),
                ('密码', {'fields': ['password', 'remote_card_password'], 'classes': ['collapse']}),
            ]
        else:
            self.fieldsets = [
                (None, {'fields': ['name', 'server_ip', 'ssh_port', 'user', 'model', 'sn_mainboard', 'sn_BIOS', 'cpu',
                                   'memory', 'disk', 'os', 'deployment_plan', 'doployment_mod', 'remote_card_ip',
                                   'remote_card_user', 'organization', 'old_asset_number', 'new_asset_number', 'owner',
                                   'owner_department', 'is_use', '_type', 'cost_center', 'checker', 'location']}),
            ]
        return super(tableAdmin, self).has_view_permission(request, obj=None)


    # 重写当操作为新增的日志，记录数据内容
    def log_addition(self, request, object, message):
        """
        Log that an object has been successfully added.

        The default implementation creates an admin LogEntry object.
        """
        orm = table.objects.filter(id=object.pk)
        all_fields_list = table._meta.get_fields()
        verbose_name_dict = {i.name: i.verbose_name for i in all_fields_list if i.name != 'comment'}
        data_dict = list(orm.values(*[i.name for i in all_fields_list]))[0]
        message = {'新增内容': {verbose_name_dict[k]: v for k,v in data_dict.items() if v}}
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=ADDITION,
            change_message=message,
        )


    # 重写当操作为修改行为的日志，记录修改后的数据内容
    def log_change(self, request, object, message, flag=1):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """
        try:
            verbose_name_list = message[0]['changed']['fields']
            name_dict = {}
            data_dict = {}
            orm = table.objects.filter(id=object.pk)
            for field in table._meta.get_fields():
                if hasattr(field, 'verbose_name'):
                    if field.verbose_name in verbose_name_list:
                        name_dict[field.name] = field.verbose_name
            for i in list(orm.values(*name_dict.keys())):
                for k, v in i.items():
                    data_dict[name_dict[k]] = v
            message = {'修改后内容': data_dict}
        except Exception:
            import traceback
            print(traceback.format_exc())
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=CHANGE,
            change_message=message,
        )


    def change_view(self, request, object_id, form_url='', extra_context=None):
        orm = table.objects.get(id=object_id)
        if orm.status == '出库':
            self.readonly_fields = ()
        else:
            self.readonly_fields = ('organization', 'location')
        return super(tableAdmin, self).change_view(request, object_id, form_url='', extra_context=None)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'object_repr', 'content_type_id', 'action_flag', 'user', 'change_message']

    date_hierarchy = 'action_time'

    list_per_page = 15

    def content_type_id(self, obj):
        return obj.content_type.app_label + ' | ' + obj.content_type.model


