# coding: utf-8
from __future__ import unicode_literals

import re
import json
import logging
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models import Sum, Max, F
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from soc.models import (
    Company as ModelCompany,
)
from soc.models import MAX_REMARK_LENGTH
from soc_user.models import RolePermissions, Roles, Permissions
from common import (
    chk_ipaddr,
    v_rack,
    Ip2Int,
    _chk_ipaddr
)

logger = logging.getLogger("soc")


class UserInfos(object):

    def __init__(self, **kwargs):
        self.context = kwargs.get('context', {})

    @property
    def user(self):
        if 'request' in self.context:
            return self.context['request'].user
        return self.context.get('user')

    @property
    def agent(self):
        if 'request' in self.context:
            return self.context['request'].user.userinfo.agent
        return self.context.get('agent')

    @property
    def company(self):
        if 'request' in self.context:
            return self.context['request'].user.userinfo.company
        return self.context.get('company')


class RoleSerializers(serializers.Serializer, UserInfos):
    name = serializers.CharField(min_length=2, max_length=10, error_messages={
        'blank': '名称不能为空',
        'min_length': '名称过短, 不能短于2个字符',
        'max_length': '名称过长, 不能长于10个字符'
    })
    enable = serializers.IntegerField()
    roles = serializers.ListField()

    def validate_name(self, data):
        if not self.instance:
            if Roles.objects.filter(name=data, agent=self.agent).exists():
                raise serializers.ValidationError("名称不能重复")
        return data

    def validate_roles(self, data):
        for role in data:
            role_id = role.get("id")
            try:
                if self.instance:
                    RolePermissions.objects.get(id=role_id, agent=self.agent)
                else:
                    Permissions.objects.get(id=role_id)
            except RolePermissions.DoesNotExist:
                raise serializers.ValidationError("Role Id 错误")
        return data

    def delete_cache(self, agent_id):
        user = User.objects.filter(userinfo__agent=agent_id).values('id')
        for i in user:
            key = 'permission_cache_user_{0}'.format(i['id'])
            cache.delete(key)

    def create_permissions(self, agent_id, role_id):
        if RolePermissions.objects.filter(agent_id=agent_id, role_id=role_id).count() == \
                Permissions.objects.count():
            return True
        for per in Permissions.objects.all():
            RolePermissions.objects.get_or_create(defaults={"enable": per.default_enable},
                                                  permissions=per, agent_id=agent_id, role_id=role_id)

    def create(self, validated_data):
        name = validated_data.get("name")
        enable = validated_data.get("enable")
        roles = validated_data.get("roles")
        role_obj = Roles.objects.create(name=name, enable=enable, agent=self.agent)
        self.create_permissions(self.agent.id, role_id=role_obj.id)
        for role in roles:
            role_id = role.get("id")
            enable = role.get("enable")
            per_obj = RolePermissions.objects.get(permissions_id=role_id, agent=self.agent, role=role_obj)
            if per_obj.enable != enable:
                per_obj.enable = enable
                per_obj.save()
        return role_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.enable = validated_data.get("enable", instance.enable)
        roles = validated_data.get('roles', [])
        instance.save()
        for role in roles:
            role_id = role.get("id")
            enable = role.get("enable")
            role_obj = RolePermissions.objects.get(id=role_id, agent=self.agent)
            if role_obj.enable != enable:
                role_obj.enable = enable
                role_obj.save()
        if roles:
            self.delete_cache(agent_id=self.agent.id)

        return instance
