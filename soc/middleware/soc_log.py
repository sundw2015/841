# coding: utf-8
from soc.models import SocLog as MoldelSocLog

def write_path(path, a, b):
    import csv
    with open('path.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([path, a, b])


class SocLog(object):
    """
    中间件 获取每个路由的操作信息
    
    通过从response里获取到视图的类 然后获取视图类的__doc__ 以及类各个请求方法的__doc__
    """
    def handle_str(self, ag):
        """
        处理字符串
        "'a'"           == > 'a'
        "\na\nb\n"         == > 'a'
        "    a    "     == > 'a'
        :param ag: 
        :return: 
        """
        if ag.startswith('"') or ag.startswith("'"):
            ag = eval(ag)
        if ag.startswith("\n"):
            ag = ag[1:]
        ag = ag.split('\n')[0]
        ag = ag.strip()
        return ag

    def get_ip(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip

    def process_response(self, request, response):
        try:
            request.user  # 有些报错信息获取不到request.user 这里进行判断 放过
        except:
            return response

        if request.path.startswith('/api/') and request.user.is_authenticated():
            try:
                # 防止有其他的response类获取不到其视图类 比如 fileresponse
                view_class = response.renderer_context['view']

            except Exception as e:
                return response

            if hasattr(view_class, 'log'):
                # 带有log的类直接返货response 不处理日志
                return response

            request_method = getattr(view_class, request.method.lower(), None)

            if not request_method:
                return response

            if isinstance(view_class, type):
                # DatatableView 的类型是type， 直接取类注释了
                request_method = view_class

            # 类注释 及 方法注释
            view_class_doc = view_class.__doc__ or ""
            request_view_doc = request_method.__doc__ or ""

            info = request_view_doc or view_class_doc

            if not all([request_view_doc, view_class_doc]):
                # 提示添加注释
                import inspect
                try:
                    line = inspect.getsourcelines(view_class.__class__)[1]
                except (TypeError, IOError):
                    print("GET DOC Error url: {}, Class: {}".format(request.path, view_class.__class__))
                else:
                    print("""当前接口无注释， 请添加
url: {}
File "{}", line {}, in process_response""".format(request.path, inspect.getsourcefile(view_class.__class__), line))

            if info:
                info = self.handle_str(info)
                view_class_doc = self.handle_str(view_class_doc)

                role = {1: "青松", 2: "管理员", 3: '企业用户'}.get(request.user.userinfo.role_type)

                ip = self.get_ip(request)
                agent = request.user.userinfo.agent
                company = request.user.userinfo.company
                level = 'info' if request.method != 'DELETE' else "warning"
                MoldelSocLog.objects.create(category=view_class_doc, role=role, level=level, info=info,
                                            user=request.user, logtype=1, agent=agent, ip=ip, company=company,
                                            url=request.path)
        return response
