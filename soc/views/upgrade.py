# coding=utf-8

import os
from rest_framework.views import APIView
from rest_framework.response import Response


UPGRADE_DIR = '/tmp/package'


class Upgrade(APIView):
    """
    系统升级
    """
    def post(self, request):
        """
        写入系统升级文件
        :param request: 
        :return: 
        """
        if 'binfile' not in request.FILES:
            return Response({"status": 500, "msg": "error"})
        name = self.request.FILES['binfile'].name
        with open(os.path.join(UPGRADE_DIR, name), 'wb') as f:
            f.write(self.request.FILES['binfile'].read())

        return Response({"status": 200, "msg": "ok"})
