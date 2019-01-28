# coding=utf-8

from django.core.management.base import BaseCommand
from soc_user.models import Permissions, PermissionUrls, Roles, Agent, UserInfo


def sync_permissions(permission, parent_id=None):
    for per in permission:
        name = per.get('name')
        urls = per.get("urls", [])
        per_obj, created = Permissions.objects.get_or_create(name=name, parent_id=parent_id)
        for url in urls:
            PermissionUrls.objects.get_or_create(permissions=per_obj, **url)
        children = per.get("children", [])
        if children:
            sync_permissions(children, per_obj.id)


class Command(BaseCommand):

    @classmethod
    def sync_user_roles(cls):
        for user in UserInfo.objects.filter(roles__isnull=True):
            if user.is_admin:
                default_role = Roles.objects.get(agent=user.agent, is_admin=1)
            else:
                default_role = Roles.objects.get(agent=user.agent, name='运维')
            user.roles.add(default_role)

    def handle(self, *args, **options):
        data = [
            {
                "name": "首页",
                "children": [
                    {
                        "name": "首页",
                        "urls": [
                            {"url": "/api/purchase/package/overview", "method": "GET"},
                            {"url": "/api/notice", "method": "GET"},
                            {"url": "/api/system/total", "method": "GET"},
                            {"url": "/api/pending_tasks", "method": "GET"},
                            {"url": "/api/recent/log", "method": "GET"},
                            {"url": "/api/recent/tickets", "method": "GET"},
                            {"url": "/api/recent/monitor", "method": "GET"},
                            {"url": "/api/recent/scans", "method": "GET"},
                            {"url": "/api/recent/attacks", "method": "GET"},
                        ]
                    }
                ]
            },
            {
                "name": "资产管理",
                "children": [
                    {
                        "name": "资产报表",
                        "children": [
                            {
                                "name": "资产总览",
                                "urls": [
                                    {"url": "/api/assets/overview", "method": "GET"},
                                    {"url": "/api/idc/map", "method": "GET"},
                                    {"url": "/api/assets/quantity", "method": "GET"},
                                    {"url": "/api/assets/proportion", "method": "GET"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "基础设施管理",
                        "children": [
                            {
                                "name": "机房和机柜",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/idc/dts", "method": "POST"}, ]},
                                    {"name": "添加机房", "urls": [{"url": "/api/idc", "method": "POST"}, ]},
                                    {"name": "编辑", "urls": [{"url": "/api/idc/", "method": "PUT"}, ]},
                                    {"name": "删除", "urls": [{"url": "/api/idc/", "method": "DELETE"}, ]},
                                    {
                                        "name": "机柜管理",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/rack/dts", "method": "POST"}, ]},
                                            {"name": "添加机柜", "urls": [{"url": "/api/rack", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/rack/", "method": "PUT"}, ]},
                                            {"name": "删除", "urls": [{"url": "/api/rack/", "method": "DELETE"}, ]},
                                        ]
                                    },
                                    {"name": "机柜视图"},
                                    {
                                        "name": "IP地址管理",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/net_ip/dts", "method": "POST"}, ]},
                                            {"name": "添加IP段", "urls": [{"url": "/api/net_ip", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/net_ip/", "method": "PUT"}, ]},
                                            {"name": "删除", "urls": [{"url": "/api/net_ip/", "method": "DELETE"}, ]},
                                        ]
                                    },

                                ]
                            },
                            {
                                "name": "库存和配件",
                                "children": [
                                    {
                                        "name": "库存管理",
                                        "children": [
                                            {"name": "查看列表",
                                             "urls": [{"url": "/api/inventory/dts", "method": "POST"}, ]},
                                            {"name": "查看库存详细信息",
                                             "urls": [{"url": "/api/inventory/", "method": "GET"}, ]},
                                            {"name": "上架",
                                             "urls": [{"url": "/api/inventory2rack", "method": "POST"}, ]},
                                            {"name": "删除(批量删除)",
                                             "urls": [{"url": "/api/inventory/", "method": "DELETE"}, ]},
                                        ]
                                    },
                                    {
                                        "name": "配件管理",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/part/dts", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/part/", "method": "PUT"}, ]},
                                            {"name": "删除", "urls": [{"url": "/api/part/", "method": "DELETE"}, ]},
                                            {"name": "类型管理", "urls": [
                                                {"url": "/api/part_type", "method": "POST"},
                                                {"url": "/api/part_type/list", "method": "POST"},
                                            ]},
                                        ]
                                    },
                                    {
                                        "name": "变更管理",
                                        "children": [
                                            {"name": "查看列表",
                                             "urls": [{"url": "/api/accessories_change/dts", "method": "POST"}, ]},
                                            {"name": "申请变更",
                                             "urls": [{"url": "/api/accessories_change", "method": "POST"}, ]},
                                            {"name": "审核",
                                             "urls": [{"url": "/api/accessories_change/", "method": "POST"}, ]},
                                            {"name": "执行",
                                             "urls": [{"url": "/api/accessories_change/", "method": "POST"}, ]},
                                            {"name": "删除",
                                             "urls": [{"url": "/api/accessories_change/", "method": "DELETE"}, ]},
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "网络拓扑",
                                "urls": [
                                    {"url": "/api/net_topo", "method": "GET"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "设备管理",
                        "children": [
                            {
                                "name": "添加主机",
                                "children": [
                                    {"name": "自动扫描", "urls": [{"url": "/api/host_discovery", "method": "POST"}, ]},
                                    {"name": "手动添加", "urls": [{"url": "/api/host", "method": "POST"}, ]},
                                    {"name": "模版导入",
                                     "urls": [{"url": "/api/multi_servers_template", "method": "POST"}, ]},
                                ]
                            },
                            {
                                "name": "主机管理",
                                "children": [
                                    {
                                        "name": "网络设备",
                                        "children": [
                                            {"name": "查看列表",
                                             "urls": [{"url": "/api/net_device/dts", "method": "POST"}, ]},
                                            {"name": "查看详细信息",
                                             "urls": [{"url": "/api/net_device/", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/net_device/", "method": "PUT"}, ]},
                                            {"name": "下架", "urls": [{"url": "/api/net_device/", "method": "DELETE"}, ]},

                                        ]
                                    },
                                    {
                                        "name": "服务器",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/server/dts", "method": "POST"}, ]},
                                            {"name": "查看详细信息", "urls": [{"url": "/api/server/", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/server/", "method": "PUT"}, ]},
                                            {"name": "下架", "urls": [{"url": "/api/server/", "method": "DELETE"}, ]},
                                        ]
                                    },
                                    {
                                        "name": "云服务器",
                                        "children": [
                                            {"name": "查看列表",
                                             "urls": [{"url": "/api/cloud_server/dts", "method": "POST"}, ]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud_server/", "method": "PUT"}, ]},
                                            {"name": "删除",
                                             "urls": [{"url": "/api/cloud_server/", "method": "DELETE"}, ]},
                                        ]
                                    },
                                ]
                            },
                            {
                                "name": "主机组管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/host_group/dts", "method": "POST"}, ]},
                                    {"name": "添加主机组", "urls": [{"url": "/api/host_group", "method": "POST"}, ]},
                                    {"name": "加入主机组", "urls": [{"url": "/api/host_group/", "method": "POST"}, ]},
                                    {"name": "编辑", "urls": [{"url": "/api/host_group/", "method": "PUT"}, ]},
                                    {"name": "删除(批量删除)", "urls": [
                                        {"url": "/api/host_group", "method": "DELETE"},
                                        {"url": "/api/host_group/", "method": "DELETE"},
                                    ]},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "地址管理",
                        "children": [
                            {
                                "name": "分配IP",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/assign_ip/dts", "method": "POST"}, ]},
                                    {"name": "分配IP地址", "urls": [{"url": "/api/assign_ip", "method": "POST"}, ]},
                                    {"name": "编辑", "urls": [{"url": "/api/assign_ip/", "method": "PUT"}, ]},
                                    {"name": "删除", "urls": [{"url": "/api/assign_ip/", "method": "DELETE"}, ]},
                                ]
                            },
                            {
                                "name": "域名管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/domain/dts", "method": "POST"}, ]},
                                    {"name": "添加域名", "urls": [{"url": "/api/domain", "method": "POST"}, ]},
                                    {"name": "编辑", "urls": [{"url": "/api/domain/", "method": "PUT"}, ]},
                                    {"name": "删除(批量删除)", "urls": [{"url": "/api/domain/", "method": "DELETE"}, ]},
                                ]
                            },
                        ]
                    }
                ]
            },
            {
                "name": "监控告警",
                "children": [
                    {
                        "name": "监控报表",
                        "children": [
                            {
                                "name": "监控总览",
                                "urls": [
                                    {"url": "/api/monitor/overview", "method": "GET"},
                                    {"url": "/api/monitor/overview/changechart", "method": "GET"},
                                    {"url": "/api/monitor/overview/dashboard", "method": "GET"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "监控管理",
                        "children": [
                            {
                                "name": "服务器监控",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/monitor/server/dts", "method": "POST"}]},
                                    {"name": "配置监控", "urls": [{"url": "/api/monitor/server", "method": "POST"}]},
                                    {"name": "暂停", "urls": [{"url": "/api/monitor/multiple/switch", "method": "PUT"}]}
                                ]
                            },
                            {
                                "name": "网络设备监控",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/monitor/net_device/dts", "method": "POST"}]},
                                    {"name": "配置监控", "urls": [{"url": "/api/monitor/net_device", "method": "POST"}]},
                                    {"name": "暂停", "urls": [{"url": "/api/monitor/multiple/switch", "method": "PUT"}]}
                                ]
                            },
                            {
                                "name": "网站访问监控",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/monitor/website/dts", "method": "POST"}]},
                                    {"name": "配置监控", "urls": [{"url": "/api/monitor/website", "method": "POST"}]},
                                    {"name": "暂停", "urls": [{"url": "/api/monitor/enable_device", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/monitor/website/", "method": "DELETE"}]}
                                ]
                            }
                        ]
                    },
                    {
                        "name": "监控模板管理",
                        "children": [
                            {
                                "name": "监控模板",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/monitor/template/dts", "method": "POST"}]},
                                    {"name": "添加", "urls": [{"url": "/api/monitor/template", "method": "POST"}]},
                                    {"name": "编辑", "urls": [{"url": "/api/monitor/template/", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/monitor/template/", "method": "DELETE"}]},
                                ]
                            },
                            {
                                "name": "告警模板",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/monitor/notify_group/dts", "method": "POST"}]},
                                    {"name": "添加", "urls": [{"url": "/api/message/notify_group", "method": "POST"}]},
                                    {"name": "编辑", "urls": [{"url": "/api/message/notify_group/", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/message/notify_group/", "method": "DELETE"}]},
                                ]
                            }
                        ]
                    }

                ]
            },
            {
                "name": "高防服务",
                "children": [
                    {
                        "name": "防御报表",
                        "children": [
                            {
                                "name": "防御总览",
                                "urls": [
                                    {"url": "/api/hw/summary/all", "method": "GET"},
                                    {"url": "/api/hw/summary/top5", "method": "GET"},
                                    {"url": "/api/hw/summary/attacks", "method": "GET"},
                                    {"url": "/api/hw/summary/history", "method": "GET"},
                                    {"url": "/api/hw/summary/comparison", "method": "GET"},
                                    {"url": "/api/hw/summary/attack_clean", "method": "GET"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "高防配置管理",
                        "children": [
                            {
                                "name": "防御集群管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/hw/cluster/dts", "method": "POST"}]},
                                    {"name": "添加", "urls": [{"url": "/api/hw/cluster", "method": "POST"}]},
                                    {"name": "编辑", "urls": [{"url": "/api/hw/cluster/", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/hw/cluster/", "method": "DELETE"}]},
                                ]
                            },
                            {
                                "name": "防御设备管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/hw/net_device/dts", "method": "POST"}]},
                                    {"name": "添加", "urls": [{"url": "/api/hw/net_device", "method": "POST"}]},
                                    {"name": "编辑", "urls": [{"url": "/api/hw/net_device/", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/hw/net_device/", "method": "DELETE"}]},
                                    {"name": "同步配置", "urls": [{"url": "/api/hw/hw_sync_device_config/", "method": "PUT"}]},
                                ]
                            },
                            {
                                "name": "防御IP管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/hw/hw_ip/dts", "method": "POST"}]},
                                    {"name": "添加", "urls": [{"url": "/api/hw/hw_ip", "method": "POST"}]},
                                    {"name": "编辑", "urls": [{"url": "/api/hw/hw_ip/", "method": "PUT"}]},
                                    {"name": "删除", "urls": [{"url": "/api/hw/hw_ip/", "method": "DELETE"}]},
                                    {"name": "同步配置","urls": [{"url": "/api/hw/hw_sync_ip_config/", "method": "PUT"}]},
                                    {"name": "查看实时数据", "urls": [{"url": "/api/hw/ip/realtime", "method": "GET"}]},
                                    {"name": "查看历史数据", "urls": [{"url": "/api/hw/ip/history", "method": "GET"}]},
                                ]
                            },
                        ]
                    }
                ]
            },
            {
                "name": "云防御",
                "children": [
                    {
                        "name": "域名管理",
                        "children": [
                            {
                                "name": "添加云防御",
                                "children": [
                                    {
                                        "name": "添加http防御",
                                        "urls": [{"url": "/api/cloud/domain", "method": "POST"}]

                                    },
                                    {
                                        "name": "添加tcp防御",
                                        "urls": [{"url": "/api/cloud/domain/transport", "method": "POST"}]

                                    },
                                ]
                            },
                            {
                                "name": "管理域名记录",

                                "children": [
                                    {
                                        "name": "http(s)防御",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/cloud/domain", "method": "GET"}]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud/domain/record", "method": "PUT"}]},
                                            {"name": "删除", "urls": [{"url": "/api/cloud/domain/record", "method": "DELETE"}]},
                                        ]
                                    },
                                    {
                                        "name": "tcp防御",
                                        "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/cloud/transport", "method": "GET"}]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud/domain/transport", "method": "PUT"}]},
                                            {"name": "删除", "urls": [{"url": "/api/cloud/domain/transport", "method": "DELETE"}]},
                                        ]
                                    },

                                ]
                            },
                            {
                                "name": "配置域名证书",
                                "children": [
                                            {"name": "查看列表", "urls": [{"url": "/api/cloud/domain/ssl", "method": "GET"}]},
                                            {"name": "添加", "urls": [{"url": "/api/cloud/domain/ssl", "method": "POST"}]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud/domain/ssl", "method": "PUT"}]},
                                            {"name": "删除", "urls": [{"url": "/api/cloud/domain/ssl", "method": "DELETE"}]},
                                        ]
                            },
                            {
                                "name": "攻击防御",
                                "children": [
                                    {
                                        "name": "开关域名服务",
                                        "children": [
                                            {"name": "开关DDoS", "urls": [{"url": "/api/cloud/domain/ddos/switch", "method": "PUT"}]},
                                            {"name": "开关CC", "urls": [{"url": "/api/cloud/domain/cc/switch", "method": "PUT"}]},
                                            {"name": "开关内容缓存", "urls": [{"url": "/api/cloud/domain/cache/switch", "method": "PUT"}]},
                                            {"name": "开关访问控制", "urls": [{"url": "/api/cloud/domain/access_filter/switch", "method": "PUT"}]},
                                        ]
                                    },
                                    {
                                        "name": "CC选项",
                                        "children": [
                                            {"name": "批量开关", "urls": [{"url": "/api/cloud/domain/multi_switch", "method": "PUT"}]},
                                            {"name": "配置选项", "urls": [{"url": "/api/cloud/domain/cc/record", "method": "PUT"}]},
                                        ]
                                    },
                                    {
                                        "name": "内容缓存",
                                        "children": [
                                            {"name": "批量开关", "urls": [{"url": "/api/cloud/domain/cache/switch/all", "method": "PUT"}]},
                                            {"name": "清除缓存", "urls": [{"url": "/api/cloud/domain/cache/refresh/record", "method": "PUT"}]},
                                            {"name": "添加不缓存的URL", "urls": [{"url": "/api/cloud/domain/cache/nocache_url", "method": "POST"}]},
                                            {"name": "删除不缓存的URL", "urls": [{"url": "/api/cloud/domain/cache/nocache_url", "method": "DELETE"}]},
                                            {"name": "配置缓存类型", "urls": [{"url": "/api/cloud/domain/cache/config", "method": "PUT"}]},
                                        ]
                                    },
                                    {
                                        "name": "访问控制策略",
                                        "children": [
                                            {"name": "查看", "urls": [{"url": "/api/cloud/domain/access_filte", "method": "GET"}]},
                                            {"name": "添加", "urls": [{"url": "/api/cloud/domain/access_filter", "method": "POST"}]},
                                            {"name": "暂停", "urls": [{"url": "/api/cloud/domain/access_filter/item_switch", "method": "PUT"}]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud/domain/access_filter", "method": "PUT"}]},
                                            {"name": "删除", "urls": [{"url": "/api/cloud/domain/access_filter", "method": "DELETE"}]},
                                        ]
                                    },
                                    {
                                        "name": "代理配置",
                                        "children": [
                                            {"name": "查看", "urls": [{"url": "/api/cloud/domain/wbconf", "method": "GET"}]},
                                            {"name": "编辑", "urls": [{"url": "/api/cloud/domain/wbconf", "method": "PUT"}]},
                                            {"name": "添加头信息", "urls": [{"url": "/api/cloud/domain/wbconf/proxy_header", "method": "PUT"}]},
                                            {"name": "删除头信息", "urls": [{"url": "/api/cloud/domain/access_filter", "method": "DELETE"}]},
                                        ]
                                    },
                                    {
                                        "name": "数据报表",
                                        "children": [
                                            {
                                                "name": "实时数据",
                                                "children": [
                                                    {"name": "查看", "urls": [{"url": "/api/cloud/report/realtime", "method": "GET"}]},
                                                ]
                                            },
                                            {
                                                "name": "历史数据",
                                                "children": [
                                                    {"name": "查看DDoS数据",
                                                     "urls": [{"url": "/api/cloud/report/ddos/history", "method": "GET"}]},
                                                    {"name": "查看访问数据数据",
                                                     "urls": [{"url": "/api/cloud/report/access/statistic", "method": "GET"}]},
                                                ]
                                            }
                                        ]
                                    }

                                ]
                            }

                        ]
                    }
                ]

            },
            {
                "name": "WAF防御",
                "children": [
                    {
                        "name": "WAF防御配置",
                        "children": [
                            {
                                "name": "基础WAF功能",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/cloud/domain/waf/default_rules", "method": "POST"}, ]},
                                    {"name": "WAF开关",
                                     "urls": [{"url": "api/cloud/domain/waf/switch", "method": "PUT"}, ]},
                                    {"name": "默认规则开关", "urls": [{"url": "api/cloud/domain/waf/default/switch", "method": "PUT"}, ]},
                                    {"name": "单条规则开关(批量开关)", "urls": [
                                        {"url": "/api/cloud/domain/waf/default_rules/switch", "method": "PUT"},
                                        {"url": "/api/cloud/domain/waf/default_rules/all_switch", "method": "PUT"}
                                    ]},
                                ]
                            },
                            {
                                "name": "高级WAF功能",
                                "children": [
                                    {"name": "查看列表",
                                     "urls": [{"url": "/api/cloud/domain/waf/custom_rules", "method": "GET"}, ]},
                                    {"name": "添加规则",
                                     "urls": [{"url": "/api/cloud/domain/waf/custom_rules", "method": "POST"}, ]},
                                    {"name": "高级规则开关",
                                     "urls": [{"url": "api/cloud/domain/waf/custom/switch", "method": "PUT"}, ]},
                                    {"name": "单条规则开关(批量开关)", "urls": [
                                        {"url": "/api/cloud/domain/waf/custom_rules/switch", "method": "PUT"},
                                        {"url": "/api/cloud/domain/waf/custom_rules/all_switch", "method": "PUT"}
                                    ]},
                                    {"name": "调整规则优先级",
                                     "urls": [{"url": "/api/cloud/domain/waf/custom_rules/priority", "method": "PUT"}, ]},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "WAF报表",
                        "children": [
                            {
                                "name": "WAF防御日志",
                                "urls": [{"url": "/api/cloud/report/waf/log", "method": "POST"}, ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "漏洞扫描",
                "children": [
                    {
                        "name": "漏洞报表",
                        "children": [
                            {
                                "name": "漏洞总览",
                                "urls": [
                                    {"url": "/api/scan/summary/all", "method": "GET"},
                                    {"url": "/api/scan/summary/top5", "method": "GET"},
                                    {"url": "/api/scan/summary/top10", "method": "GET"},
                                    {"url": "/api/scan/summary/vul_week_line", "method": "GET"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "网站漏洞扫描",
                        "children": [
                            {
                                "name": "扫描任务管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/scan/scan_task/dts", "method": "POST"}]},
                                    {"name": "新建扫描", "urls": [{"url": "/api/scan/scan_task ", "method": "POST"}]},
                                    {"name": "修改扫描", "urls": [{"url": "/api/scan/scan_task/ ", "method": "PUT"}]},
                                    {"name": "删除扫描", "urls": [{"url": "/api/scan/scan_task/ ", "method": "DELETE"}]},
                                    {"name": "查看历史", "urls": [{"url": "/api/scan/scan_result/dts ", "method": "POST"}]},
                                ]
                            },
                            {
                                "name": "网站漏洞管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/scan/domainscan/security_threat/dts", "method": "POST"}]},
                                    {"name": "查看TOP5", "urls": [{"url": "/api/scan/domain_scan/vul_type_top5 ", "method": "GET"}]},
                                    {"name": "查看分布", "urls": [{"url": "/api/scan/domain_scan/vul_level_count ", "method": "GET"}]},
                                ]
                            }
                        ],

                    },
                    {
                        "name": "主机漏洞扫描",
                        "children": [
                            {
                                "name": "扫描任务管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/scan/scan_host_task/dts", "method": "POST"}]},
                                    {"name": "新建扫描", "urls": [{"url": "/api/scan/scan_task ", "method": "POST"}]},
                                    {"name": "修改扫描", "urls": [{"url": "/api/scan/scan_task/ ", "method": "PUT"}]},
                                    {"name": "删除扫描", "urls": [{"url": "/api/scan/scan_task/ ", "method": "DELETE"}]},
                                    {"name": "查看历史", "urls": [{"url": "/api/scan/scan_host_history/dts ", "method": "POST"}]},
                                ]
                            },
                            {
                                "name": "主机漏洞管理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/scan/host/security_threat/dts", "method": "POST"}]},
                                    {"name": "查看TOP5", "urls": [{"url": "/api/scan/host/vul_type_top5 ", "method": "GET"}]},
                                    {"name": "查看分布", "urls": [{"url": "/api/scan/host/vul_level_count ", "method": "GET"}]},
                                ]
                            }
                        ],

                    },
                ]
            },
            {
                "name": "终端安全",
                "children": [
                    {
                        "name": "Agent部署",
                        "children": [
                            {"name": "查看列表", "urls": [{"url": "/api/hids/agents/dts", "method": "POST"}, ]},
                            {"name": "添加Agent", "urls": [{"url": "/api/hids/agents", "method": "POST"}, ]},
                            {"name": "配置", "urls": [{"url": "/api/hids/agents/", "method": "PUT"}, ]},
                            {"name": "删除", "urls": [{"url": "/api/hids/agents/", "method": "DELETE"}, ]},
                        ]
                    },
                    {
                        "name": "文件完整性检查",
                        "children": [
                            {
                                "name": "防篡改防护选项",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/hids/syscheck/dts", "method": "POST"}, ]},
                                    {"name": "添加防护目标", "urls": [{"url": "/api/hids/syscheck", "method": "POST"}, ]},
                                    {"name": "配置", "urls": [{"url": "/api/hids/syscheck/", "method": "PUT"}, ]},
                                    {"name": "删除", "urls": [{"url": "/api/hids/syscheck/", "method": "DELETE"}, ]},
                                ]
                            },
                            {
                                "name": "恢复源配置",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/hids/recover_source/dts", "method": "POST"}, ]},
                                    {"name": "添加恢复源", "urls": [{"url": "/api/hids/recover_source", "method": "POST"}, ]},
                                    {"name": "配置", "urls": [{"url": "/api/hids/recover_source/", "method": "PUT"}, ]},
                                    {"name": "删除", "urls": [{"url": "/api/hids/recover_source/", "method": "DELETE"}, ]},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "日志监控",
                        "children": [
                            {
                                "name": "查看日志",
                                "urls": [{"url": "/api/hids/agents/syslog", "method": "POST"}, ]
                            }
                        ]
                    },
                    {
                        "name": "rootkit检测",
                        "children": [
                            {
                                "name": "rootkit检查选项",
                                "children": [
                                    {"name": "查看列表",
                                     "urls": [{"url": "/api/hids/rootcheck/dts", "method": "POST"}, ]},
                                    {"name": "添加",
                                     "urls": [{"url": "/api/hids/rootcheck", "method": "POST"}, ]},
                                    {"name": "配置", "urls": [{"url": "/api/hids/rootcheck/", "method": "PUT"}, ]},
                                    {"name": "删除",
                                     "urls": [{"url": "/api/hids/rootcheck/", "method": "DELETE"}, ]},
                                ]
                            },
                            {
                                "name": "rootkit上报详情",
                                "children": [
                                    {"name": "查看列表",
                                     "urls": [{"url": "/api/hids/rootcheck_log/dts", "method": "POST"}, ]},
                                ]
                            },
                        ]
                    }
                ]
            },
            {
                "name": "网络安全",
                "children": [
                    {
                        "name": "网络安全功能",
                        "children": [
                            {
                                "name": "主机管理",
                                "children": [

                                ]
                            },
                            {
                                "name": "基础IDS功能",
                                "children": [
                                    {"name": "IDPS 开关", "urls": [{"url": "/api/nids/switch", "method": "PUT"}, ]},
                                    {"name": "IDPS 切换模式", "urls": [{"url": "/api/nids/work_mode/switch", "method": "PUT"}, ]},
                                    {"name": "查看规则集列表", "urls": [{"url": "/api/nids/default_ruleset/dts", "method": "POST"}, ]},
                                    {"name": "查看规则集配置", "urls": [{"url": "/api/nids/default_rule/dts", "method": "POST"}, ]},
                                    {"name": "启用/暂停规则集合", "urls": [{"url": "/api/nids/default_ruleset/switch", "method": "PUT"}, ]},
                                    {"name": "启用/暂停全部规则集合", "urls": [{"url": "/api/nids/default_ruleset/all_switch", "method": "PUT"}, ]},
                                    {"name": "修改规则配置", "urls": [{"url": "/api/nids/default_rule/switch", "method": "PUT"}, ]},

                                ]
                            },
                            {
                                "name": "高级IDS功能",
                                "children": [
                                    {"name": "查看自定义规则列表",
                                     "urls": [{"url": "/api/nids/custom_rule/dts", "method": "POST"}, ]},
                                    {"name": "添加自定义规则",
                                     "urls": [{"url": "/api/nids/custom_rule", "method": "POST"}, ]},
                                    {"name": "编辑自定义规则",
                                     "urls": [{"url": "/api/nids/custom_rule/", "method": "PUT"}, ]},
                                    {"name": "删除自定义规则",
                                     "urls": [{"url": "/api/nids/custom_rule/", "method": "DELETE"}, ]},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "数据报表",
                        "children": [
                            {
                                "name": "威胁日志",
                                "urls": [{"url": "/api/nids/report/log/dts", "method": "POST"}]
                            }
                        ]
                    },
                ]
            },
            {
                "name": "服务支持",
                "children": [
                    {
                        "name": "公司管理",
                        "children": [
                            {"name": "查看列表", "urls": [{"url": "/api/company/dts", "method": "POST"}, ]},
                            {"name": "添加", "urls": [{"url": "/api/company/", "method": "POST"}, ]},
                            {"name": "编辑", "urls": [{"url": "/api/company/", "method": "PUT"}, ]},
                            {"name": "删除", "urls": [{"url": "/api/company/", "method": "DELETE"}, ]},
                        ]
                    },
                    {
                        "name": "用户管理",
                        "children": [
                            {"name": "查看列表", "urls": [{"url": "/api/user/dts", "method": "POST"}, ]},
                            {"name": "添加", "urls": [{"url": "/api/user/", "method": "POST"}, ]},
                            {"name": "编辑(锁定)", "urls": [{"url": "/api/user/", "method": "PUT"}, ]},
                            {"name": "删除", "urls": [{"url": "/api/user/", "method": "DELETE"}, ]},
                        ]
                    },
                    {
                        "name": "消息管理",
                        "children": [
                            {"name": "查看列表", "urls": [{"url": "/api/message/dts", "method": "POST"}, ]},
                            {"name": "标记已读", "urls": [{"url": "/api/message", "method": "PUT"}, ]},
                        ]
                    },
                    {
                        "name": "工单管理",
                        "children": [
                            {
                                "name": "工单申请",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/ticket_apply/dts", "method": "POST"}, ]},
                                    {"name": "添加", "urls": [{"url": "/api/tickets", "method": "POST"}, ]},
                                ]
                            },
                            {
                                "name": "工单处理",
                                "children": [
                                    {"name": "查看列表", "urls": [{"url": "/api/ticket_handle/dts", "method": "POST"}, ]},
                                    {"name": "添加", "urls": [{"url": "/api/tickets", "method": "POST"}, ]},
                                    {"name": "修改状态", "urls": [{"url": "/api/tickets/", "method": "PUT"}, ]},
                                ]
                            }
                        ]
                    },
                ]
            },
            {
                "name": "服务购买",
                "urls": [
                    {"url": "/api/purchase/services", "method": "GET"},
                    {"url": "/api/purchase/service/count", "method": "POST"},
                    {"url": "/api/purchase/pay_now", "method": "POST"},
                    {"url": "/api/purchase/shopping_cart", "method": "POST"},
                ]
            }
        ]
        roles = ["管理员", "客服专员", "商务专员", "技术支持", "运维", "财务"]
        sync_permissions(data)

        for agent in Agent.objects.all():
            for role in roles:
                role_obj, created = Roles.objects.get_or_create(agent=agent, name=role, defaults={"enable": 1})
                if role == '管理员':
                    role_obj.is_admin = 1
                    role_obj.save()
        self.sync_user_roles()
