# coding=utf-8
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.datatable import DatatableView
from soc_user.models import RolePermissions, Permissions, Roles
from soc.serializers import RoleSerializers
from utils.auth import AllowAdminWithPassword

logger = logging.getLogger("console")


def re_per(per_list, per_tree=list(), parent_list=list(), max_re=5, re=0):
    """
    递归 构建权限树
    :param per_list: 原始权限列表
    :param per_tree: 权限树
    :param parent_list: 当前递归所需的父级权限列表
    :param max_re: 最大递归层数
    :param re: 当前递归层数
    :return:
    """

    re += 1
    if re > max_re:
        return per_tree
    need_remove = []
    if not per_list:
        return per_tree
    if not per_tree:
        for index, per in enumerate(per_list):
            if per.get('parent_id') is None:
                per['re'] = re
                per_tree.append(per)
                need_remove.append(per)
                parent_list.append(per)
        for i in need_remove:
            per_list.remove(i)

    else:
        new_parent_list = []
        for parent in parent_list:
            need_remove = []
            for role in filter(lambda x: x.get("parent_id") == parent.get("permission_id"), per_list):
                role['re'] = re
                parent.get("children").append(role)
                need_remove.append(role)
                new_parent_list.append(role)
            for i in need_remove:
                per_list.remove(i)
        parent_list = new_parent_list

    return re_per(per_list, per_tree, parent_list=parent_list, max_re=max_re, re=re)


class RolePermissionDetail(APIView):
    """权限管理"""
    permission_classes = (AllowAdminWithPassword,)
    """
   {
    "status": 200,
    "data": [
        {
            "parent_id": null,
            "enable": 1,
            "name": "首页",
            "re": 1,
            "url": "/api/soc/1",
            "permission_id": 1,
            "children": [
                {
                    "parent_id": 1,
                    "enable": 1,
                    "name": "总览",
                    "re": 2,
                    "url": "/api/soc/1/1",
                    "permission_id": 2,
                    "children": [
                        {
                            "parent_id": 2,
                            "enable": 1,
                            "name": "总览报表",
                            "re": 3,
                            "url": "/api/soc/1/1",
                            "permission_id": 3,
                            "children": [],
                            "id": 3,
                            "method": "GET"
                        }
                    ],
                    "id": 2,
                    "method": "GET"
                }
            ],
            "id": 1,
            "method": "GET"
        }
    ]
}

    """
    @staticmethod
    def create_permissions(agent_id, role_id):
        if RolePermissions.objects.filter(agent_id=agent_id, role_id=role_id).count() == \
                Permissions.objects.count():
            return True
        for per in Permissions.objects.all():
            RolePermissions.objects.get_or_create(defaults={"enable": per.default_enable},
                                                  permissions=per, agent_id=agent_id, role_id=role_id)

    def get(self, request, role_id):
        """获取权限管理信息"""
        agent_id = request.user.userinfo.agent_id
        if not Roles.objects.filter(id=role_id).exists():
            return Response({"status": 500, "msg": "Role Id 错误"})
        self.create_permissions(agent_id, role_id)
        role_permissions = RolePermissions.objects.filter(
            agent_id=agent_id, role_id=role_id)
        permission_list = []
        for role_obj in role_permissions:
            data = {
                "id": role_obj.id,
                "permission_id": role_obj.permissions_id,
                "name": role_obj.permissions.name,
                "parent_id": role_obj.permissions.parent_id,
                "enable": role_obj.enable,
                "children": [],
                "show": False
            }
            permission_list.append(data)
        data = re_per(permission_list, [], [])
        return Response({"status": 200, "data": data})

    def put(self, request, role_id):
        """修改权限"""
        agent = request.user.userinfo.agent
        agent_id = agent.id
        try:
            role = Roles.objects.get(id=role_id, agent_id=agent_id)
        except Roles.DoesNotExist:
            return Response({"status": 500, "msg": "Role Id 错误"})

        if role.is_admin:
            return Response({"status": 500, "msg": "管理员权限不能修改"})

        serializer = RoleSerializers(
            instance=role, data=request.data, context={"agent": agent})
        if serializer.is_valid():
            serializer.save()
        else:
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            return Response(context)
        return Response({"status": 200, "msg": "修改成功"})

    def delete(self, request, role_id):
        """删除权限"""
        agent = request.user.userinfo.agent
        try:
            role = Roles.objects.get(id=role_id, agent=agent)
        except Roles.DoesNotExist:
            return Response({"status": 500, "msg": "Role Id 错误"})
        if role.is_admin:
            return Response({"status": 500, "msg": "管理员权限不能删除"})

        if role.userinfo_set.count() > 0:
            return Response({"status": 500, "msg": "使用中的权限组不能删除"})

        role.delete()
        return Response({"status": 200, "msg": "删除成功"})


class RolePermissionSelectList(APIView):
    """权限管理"""

    def get(self, request):
        """获取权限管理列表"""
        agent = request.user.userinfo.agent
        data = Roles.objects.filter(agent=agent, enable=1).values("id", "name")
        return Response({"status": 200, "data": data})


class RolePermissionList(APIView):
    """权限管理"""
    permission_classes = (AllowAdminWithPassword, )

    def get(self, request):
        """获取管理权限信息"""
        permission_list = []
        for i in Permissions.objects.values('id', 'parent_id', 'name'):
            i.update({
                "permission_id": i['id'],
                "children": [],
                "enable": 1,
                "show": False,

            })
            permission_list.append(i)
        data = re_per(permission_list, [], [])
        return Response({"status": 200, "data": data})

    def post(self, request):
        """创建角色"""
        agent = request.user.userinfo.agent
        serializer = RoleSerializers(
            data=request.data, context={"agent": agent})
        if serializer.is_valid():
            serializer.save()
        else:
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            return Response(context)

        return Response({"status": 200, "msg": '创建成功'})


class RoleList(DatatableView):
    """角色列表"""
    render_columns = [
        ("id", "id", 0),
        ("name", "name", 1),
        ("enable", "enable", 0),
        ("is_admin", "is_admin", 0),
        ("users", "id", 0),
    ]

    model = Roles

    def get_initial_queryset(self):
        agent_id = self.request.user.userinfo.agent_id
        inventory = self.model.objects.filter(agent_id=agent_id)
        return inventory

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        qs 为查询集合
        """
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            data_dict['users'] = item.userinfo_set.count()
            data.append(data_dict)
        return data
