# coding=utf-8
import logging
from soc_user.models import RolePermissions, PermissionUrls
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from utils.black_white_ip import get_blackip_list, get_whiteip_list
from soc.models import Agent
from datetime import timedelta
from django.utils import timezone
from soc_system.models import BlackIPList

logger = logging.getLogger("soc")


def permission_cache(timeout=60 * 60):
    """
    soc 权限缓存装饰器
     :timeout 缓存超时时间 单位秒 默认 一小时
    """

    def decorator(func):
        def wrapper(*args, **kw):
            request = args[1]
            cache_key = "permission_cache_user_{0}".format(request.user.id)
            data = cache.get(cache_key)
            # logger.debug('permission_cache 获取缓存 key: {0}'.format(cache_key))
            if data is None:
                logger.debug('permission_cache 未命中缓存 key: {0}'.format(cache_key))
                data = func(*args, **kw)
                cache.add(cache_key, data, timeout)
            return data

        return wrapper

    return decorator


class Permission(object):

    WHITE_URL = [
        '/api/system/menus',
        '/api/system/total',
        '/api/system/version',
        '/api/system/nodes/clear/api/parent',
        '/api/system/nodes/p_status',
    ]

    @classmethod
    @permission_cache()
    def get_permissions(cls, request):
        try:
            roles = request.user.userinfo.roles.all()
            role_tree = {}
            role_permissions = RolePermissions.objects.filter(agent_id=request.user.userinfo.agent_id, role__in=roles)
            permission_ids = []
            permission_dict = {}
            for role in role_permissions:
                permission_ids.append(role.permissions_id)
                role_key = role.permissions_id
                if not permission_dict.get(role_key, 0):
                    permission_dict[role_key] = role.enable
            permission_urls = PermissionUrls.objects.filter(permissions_id__in=permission_ids)\
                .values('url', 'method', 'permissions_id')
            for url in permission_urls:
                role_key = "{}_{}".format(url.get('url'), url.get('method'))
                role_tree[role_key] = permission_dict[url.get('permissions_id')]
            return role_tree
        except Exception as e:
            logger.error(e)
        return {}

    @classmethod
    def reconver_url(cls, path):
        """
        将url 最后的id位转为/ 用于模糊匹配
        /api/server/1
        /api/server/2     ===> /api/server/
        /api/server/3

        :param path: /api/server/22
        :return: /api/server/
        """
        end = path.split('/')[-1]
        try:
            int(end)
        except (TypeError, ValueError):
            return path
        else:
            return "/".join(path.split('/')[:-1]) + '/'

    @classmethod
    def process_request(cls, request):
        if request.path in cls.WHITE_URL:
            return

        # 只允许代理商管理员访问系统设置
        if request.path.startswith('/api/system/nodes/auth'):
            return

        if request.path.startswith('/api/system') and isinstance(request.user, AnonymousUser):
            return JsonResponse({"msg": "您所在的角色无法使用该接口", "code": 10001}, status=403)

        if request.path.startswith('/api/system') and request.user.userinfo.is_not_agent_admin:
            return JsonResponse({"msg": "您所在的角色无法使用该接口", "code": 10001}, status=403)
        
        path = cls.reconver_url(request.path)
        role_key = "{}_{}".format(path, request.method)
        if request.user.id:
            if cls.get_permissions(request).get(role_key) == 0:
                # 返回值 0: 拒绝, 1: 运行, None: 未定义权限
                return JsonResponse({"msg": "您所在的角色无法使用该接口", "code": 10001}, status=403)


class BlackIP(object):
    """
    验证进来的iP是否在黑白名单上
    
    """

    def process_request(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if x_forwarded_for:
            real_ip = x_forwarded_for.split(',')[0]
        else:
            real_ip = request.META.get('REMOTE_ADDR', '')

        if not real_ip:
            return JsonResponse({"msg": "发生未知错误,获取不到ip，请联系管理员", "status": 403}, status=200)

        if isinstance(request.user, AnonymousUser):
            host = request.META['HTTP_HOST']
            try:
                agent = Agent.objects.get(web_domain=host)
            except Agent.DoesNotExist:
                return None
        else:
            agent = request.user.userinfo.agent

        blackip = cache.get("blackip_{0}".format(real_ip))

        if blackip is True:
            # 黑名单 拦截
            msg = "IP属于黑名单,无法操作，请联系管理员"
            return JsonResponse({"msg": msg, "error": msg, "status": 403}, status=200)
        elif blackip is False:
            # 白名单 放行
            return None

        else:
            # 没在缓存里
            fail_ban_time = agent.fail_ban_time  # 禁止时间
            delete_time = timezone.now() - timedelta(seconds=fail_ban_time)
            # 手动添加黑名单
            black_ip_type1 = BlackIPList.objects.filter(ip=real_ip, is_black=1, type=1)
            # 自动添加黑名单已经过期
            black_ip_type2 = BlackIPList.objects.filter(ip=real_ip, is_black=1, start_time__lt=delete_time, type=0)
            # 自动添加黑名单 未过期
            black_ip_type3 = BlackIPList.objects.filter(ip=real_ip, is_black=1, start_time__gte=delete_time, type=0)

            if BlackIPList.objects.filter(ip=real_ip, is_black=2):
                # 在数据库的白名单里
                cache.set("blackip_{0}".format(real_ip), False)
                # 添加到缓存里 标记为 False 放行
                return None

            elif black_ip_type1:
                # 手动添加的黑名单 添加到缓存里 标记为 True
                cache.set("blackip_{0}".format(real_ip), True)

            elif black_ip_type2:
                # 自动添加到黑名单 并且时间已经过期 不算黑名单
                return None

            elif black_ip_type3:
                # 自动添加到黑名单 时间未过期
                msg = "IP属于黑名单，无法操作，请联系管理员"
                return JsonResponse({"msg": msg, "error": msg, "status": 403}, status=200)
            else:
                # 既不是黑名单也不是白名单
                cache.set("blackip_{0}".format(real_ip), False)
                return None
