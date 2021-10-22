from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from process.models import table as _table
import dingtalkchatbot.chatbot as cb
from django.contrib.auth.models import User
import datetime
from libs.ldap_pack import search_user_info

# 初始化钉钉机器人
webhook = "https://oapi.dingtalk.com/robot/send?access_token=91d1eae7558afbce70054eb50b3e1ca245354f081ca6326a9a2f342187d957ec"
dingtalk = cb.DingtalkChatbot(webhook)


@login_required
def table(request):
    username = search_user_info(request.user.username).get('name')
    return render(request, 'process/table.html',{'user': username,
                                                 'path1': 'process',
                                                 'path2': 'process_table',
                                                 'page_name1': '流程管理',
                                                 'page_name2': '流程表',})


@login_required
def table_data(request):
    username = search_user_info(request.user.username).get('name')
    tableData = []
    print(request.user.has_perm('process.can_view_all'))
    if not request.user.has_perm('process.can_view_all'):
        orm = _table.objects.filter(name=username)
    else:
        orm = _table.objects.all()

    for i in orm:
        tableData.append({
            'id': i.id,
            'name': i.name,
            'cities': i.cities,
            '_type': i._type,
            'description': i.description,
            'result': i.result,
            'status': i.status,
            'processor': i.processor,
            'create_time': str(i.create_time).split('.')[0],
            'finish_time': str(i.finish_time).split('.')[0],
        })
    return JsonResponse({'code': -1, 'tableData': tableData})


@login_required
def table_save(request):
    username = search_user_info(request.user.username).get('name')
    data = json.loads(request.body)
    cities = data.get('cities')
    _type = data.get('_type')
    description = data.get('description')
    orm = _table(name=username, cities=cities, _type=_type, description=description)
    orm.save()
    # 发送钉钉提醒
    text = f'**[{orm.id}]** **{username}** 申请了一条 **{cities}** 的 **{_type}** ○ '
    dingtalk.send_markdown(title='等待完成', text=text)
    return JsonResponse({'code': 0, 'msg': '操作成功'})


@login_required
def table_commit(request):
    user_info = search_user_info(request.user.username)
    username = user_info.get('name')
    telephone = user_info.get('telephone')
    data = json.loads(request.body)
    id = data.get('id')
    result = data.get('result')
    orm = _table.objects.select_for_update().get(id=id)
    orm.status = '已完成'
    orm.processor = username
    if result:
        orm.result = result
    orm.finish_time = datetime.datetime.now()
    orm.save()
    text = f'**[{orm.id}]** **{username}** 完成了一条 **{orm.cities}** 的 **{orm._type}** √ 请查收'
    dingtalk.send_markdown(title='等待完成', text=text, at_mobiles=[telephone])
    return JsonResponse({'code': 0, 'msg': '操作成功'})


@login_required
def table_del(request):
    username = search_user_info(request.user.username).get('name')
    data = json.loads(request.body)
    id = data.get('id')
    orm = _table.objects.select_for_update().get(id=id)
    orm.delete()
    text = f'**[{orm.id}]** **{username}** 撤销了一条 **{orm.cities}** 的 **{orm._type}** ×'
    dingtalk.send_markdown(title='等待完成', text=text)
    return JsonResponse({'code': 0, 'msg': '撤销成功'})