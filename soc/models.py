# coding=utf-8
from __future__ import unicode_literals
import uuid
import socket
import struct

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from django.core.cache import cache
import logging
import time
logger = logging.getLogger('soc')


def Int2Ip(i):
    return socket.inet_ntoa(struct.pack("!I", i))

# 参数 remark 的最大长度
MAX_REMARK_LENGTH = 8196
SN_PREFIX_RACK = 'RAC_'
SN_PREFIX_SERVER = 'SER_'
SN_PREFIX_NET_DEVICE = 'NDE_'
SN_PREFIX_INVENTORY = 'INV_'
SN_PREFIX_CLOUD_SERVER = 'CSR_'
SN_LENGTH = 8

AssetChoices = (
    (1, u"库存"),
    (2, u"上架")
)

terminal_type = {
    1: "电脑",
    2: "手机",
    3: "打印机",
    4: "摄像头",
    5: "其他",
}

terminal_grade = {
    1: "一级",
    2: "二级",
    3: "三级",
    4: "四级",
    5: "五级"
}


class Agent(models.Model):
    """代理商表"""

    name = models.CharField(max_length=128, unique=True, null=False)
    # 代理商激活状态
    status = models.IntegerField(default=0)  # 0 is inactive; 1 is active
    # iframe系统中的groups表的ID, 对应代理商
    agent_id = models.IntegerField(null=True)
    # iframe系统中的crmUser表的信息, 对应代理商付费的账号
    crm_user_id = models.IntegerField(null=True)
    crm_user_name = models.CharField(max_length=128, null=True)
    license = models.CharField(max_length=128, null=True)
    # 标识是否为青松账号,1是0否;
    # 判断青松账号也可从Agent ID为1来判断
    # is_super_admin = models.IntegerField(default=0)
    # 代理商标题
    title = models.CharField(max_length=120, null=True)
    # 前端页面显示的title 和 logo
    web_title = models.CharField(max_length=120, default='云松')
    web_logo = models.ImageField(default='logo/logo.svg', upload_to='images/logo')
    # 代理商自己的域名
    web_domain = models.CharField(max_length=256, null=True)
    # 是否开启七层防御的iframe 默认开启
    enable_iframe = models.BooleanField(default=True)
    # 来自crm的token
    token = models.CharField(max_length=64, null=True)
    # 青松 token
    qs_token = models.CharField(max_length=128, null=True)
    qs_token_secret = models.CharField(max_length=128, null=True)
    qs_api_timeout = models.IntegerField(default=60, null=True)
    # 代理商公钥
    ssl_pub_key = models.TextField(null=True)
    # 代理商唯一标识
    key = models.CharField(max_length=64, default=uuid.uuid4)
    # 青松API token
    qs_api_token = models.CharField(max_length=64, blank=True, null=True)

    # IP登录失败限制次数
    fail_count = models.IntegerField(default=10)
    # IP登录失败限制时间 单位秒
    fail_range_time = models.IntegerField(default=180)
    # IP登录失败锁定时间 单位秒
    fail_ban_time = models.IntegerField(default=3600)

    # IP注册时间显示 单位秒
    register_time = models.IntegerField(default=180)
    # IP注册单位时间内限制注册账号数
    register_count = models.IntegerField(default=5)
    # 是否允许注册 1 允许注册 0 不开放注册
    register_allow = models.IntegerField(default=1)
    # 是否允许登陆 1 允许登陆 0 不允许登陆
    login_allow = models.IntegerField(default=1)
    # 登陆方式 username,email,phone,wechat 以逗号分隔
    login_type = models.CharField(max_length=128, default='username,email,phone,wechat')
    # 登录超时, 单位秒，默认60分钟（3600秒）
    login_timeout = models.IntegerField(default=3600)
    # 可通过密码找回解锁 1为允许 2为不允许
    is_find_password = models.IntegerField(default=1)
    # 备案编号
    record_number = models.CharField(max_length=128, null=True, blank=True)
    # 服务电话
    server_phone = models.CharField(max_length=64, null=True, blank=True)
    # 代理商邮箱
    email = models.CharField(max_length=128, null=True, blank=True, default='')

    @staticmethod
    def ban_key(ip):
        return "ban_ip_{0}".format(ip)

    def ban_ip(self, ip, ban_time=None):
        if not ban_time:
            ban_time = self.fail_ban_time
        logger.error("代理商下: {}-{} 超出最大登录失败次数，禁止登录{}秒".format(self.name, ip, ban_time))
        cache.add(self.ban_key(ip), 'ban', ban_time)

    def uban(self, ip):
        cache.delete(self.ban_key(ip))

    def is_ban(self, ip):
        return bool(cache.get(self.ban_key(ip), False))

    def login_fail_ip(self, ip):
        key = "login_fail_ip_{0}".format(ip)
        fail_count = cache.get(key)
        if not fail_count:
            cache.add(key, 1, self.fail_range_time)
            if 1 >= self.fail_count:
                self.ban_ip(ip)
        else:
            fail_count = cache.incr(key)
            if fail_count >= self.fail_count:
                self.ban_ip(ip)

    def register_ip(self, ip):
        # 举个例子
        # 每注册一次，都记录下注册的时间，超过3分钟的，就删掉，这样在记录的，都是在3分钟内注册的，只判定个数就好了
        key = "register_ip_{0}".format(ip)
        last_time = cache.get(key)
        if not last_time:
            cache.add(key, str(int(time.time())), self.register_time*2)
        else:
            last_times = map(int, last_time.split(','))
            now = int(time.time())
            new_last_times = []
            for i in last_times:
                # 剔除掉超时的
                if now - i <= self.register_time:
                    new_last_times.append(i)
            new_last_times.append(int(time.time()))
            new_last_time = ','.join(map(str, new_last_times))
            cache.delete(key)
            cache.add(key, new_last_time, self.register_count*2)

    def ban_register(self, ip):
        # 检查是否注册禁止
        key = "register_ip_{0}".format(ip)
        last_time = cache.get(key)
        if last_time:
            last_times = map(int, last_time.split(','))
            now = int(time.time())
            new_last_times = []
            for i in last_times:
                if now - i <= self.register_time:
                    new_last_times.append(i)
            if len(new_last_times) >= self.register_count:
                return False
        return True

    class Meta:
        db_table = 'agent'
        verbose_name = "代理商"

    def __unicode__(self):
        return self.name


class Company(models.Model):
    """
    公司客户表
    """
    agent = models.ForeignKey(Agent)
    # 公司名称
    name = models.CharField(max_length=120)
    # 公司地址
    address = models.CharField(max_length=256, blank=True, null=True)
    # 公司电话
    phone = models.CharField(max_length=256, blank=True, null=True)
    # 公司邮箱
    email = models.EmailField(blank=True, null=True)
    # 公司唯一标识
    key = models.CharField(max_length=64, default=uuid.uuid4)
    # 青松API token
    qs_api_token = models.CharField(max_length=64, blank=True, null=True)
    # 公司类型标识，1正常公司，0匿名公司
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'company'
        verbose_name = "公司客户"

    def __unicode__(self):
        return self.name


class SocLog(models.Model):
    """日志表"""
    LOGTYPE = ((1, '操作日志'), (2, '登陆日志'), (3, "注册日志"))
    STATUS = ((1, '登陆成功'), (2, '登陆失败'))
    # 时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 操作所属类
    category = models.CharField(max_length=128)
    # 操作等级 delete 为waring
    level = models.CharField(max_length=128)
    # 操作日志
    info = models.CharField(max_length=128)
    user = models.ForeignKey(User, null=True, blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    # 日志操作的角色 管理员 or 用户
    role = models.CharField(max_length=64, default='', null=True)
    # 日志类型
    logtype = models.IntegerField(choices=LOGTYPE, null=True, blank=True)
    # 登陆状态 登陆日志时才有
    login_status = models.IntegerField(choices=STATUS, null=True, blank=True)
    # IP
    ip = models.CharField(max_length=32, null=True, blank=True)
    # 接口路径
    url = models.CharField(max_length=256, null=True, blank=True, default='')

    class Meta:
        db_table = 'soc_log'
        verbose_name = "soc日志"

    def __unicode__(self):
        return self.category


class Message(models.Model):

    title = models.CharField(max_length=128)
    content = models.TextField()
    # 消息类型: 0: 其他消息, 1: 安全扫描, 2: 监控告警 
    type = models.IntegerField()
    # 消息等级, 1非常紧急,2紧急,3一般,4不紧急
    priority = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否阅读: 0未阅读,1已阅读
    is_read = models.IntegerField()
    # 对应用户
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = "message"
        verbose_name = "消息"



class Perms(models.Model):
    """权限表"""

    name = models.CharField(max_length=128)
    perms_id = models.CharField(max_length=128, unique=True)
    # priority = models.IntegerField()

    class Meta:
        db_table = 'perms'
        verbose_name = "模块权限"

    def __unicode__(self):
        return self.name


class AgentPerms(models.Model):
    """Agent和Perms权限对应表"""

    perms = models.ForeignKey(Perms)
    agent = models.ForeignKey(Agent)

    class Meta:
        db_table = 'agent_perms'
        verbose_name = "代理商权限"
        unique_together = ('agent', 'perms')

    def __unicode__(self):
        return self.agent.name + ':' + self.perms.name