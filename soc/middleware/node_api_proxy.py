#coding=utf-8
import json
from django.http import JsonResponse
from utils.api import NodeApi
from soc_system import models
"""
代理访问子中心API接口
"""
class NodeAPIProxy(object):
    """
    代理访问子中心API接口中间件
    """
    @classmethod
    def process_request(cls, request):
        """
        通过查询前端传递的参数中是否为调用子节点 直接在中间件中调用子节点API并返回数据
        """
        if request.method == "GET":
            data = request.GET
        elif request.method == "POST":
            data = request.POST
        else:
            return
        sub_id = data.get('node_parent_id')  # 跨级子中心对应的上级中心 ID
        node_uuid = data.get('node_uuid')  # 所属中心的uuid
        # 无对应参数，pass该请求
        if not node_uuid:
            return     
        agent = request.user.userinfo.agent
        try:
            sub_id = int(sub_id)
        except (TypeError, ValueError):
            sub_id = 0

        try:
            node_obj = models.Node.objects.get(uuid=node_uuid)
            role = node_obj.role
        except models.Node.DoesNotExist:
            node_obj = None
            role = None
        # 如果为当前中心 pass
        if role == 'self':
            return
        # 如果为当前中心的下级
        if node_obj:
            data = data.copy()
            data.pop("node_uuid")
        # 如果为当前中心的下下级
        else:
            try:
                node_obj = models.Node.objects.get(id=sub_id, agent=agent)
            except models.Node.DoesNotExist:
                return JsonResponse({"status": 500, "msg": "该中心不存在", "error": "该三级中心不存在"})
            data = data.copy()
            data.pop("node_parent_id")

        node_api = NodeApi(base_url='http://{}:{}'.format(node_obj.ip, node_obj.port),
                           secret_id=node_obj.secret_id, secret_key=node_obj.secret_key)
        result = node_api.fetch(method=request.method, api=request.path, params=data)
        return JsonResponse(result)
