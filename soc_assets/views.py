# coding=utf-8

from rest_framework.response import Response
from rest_framework.views import APIView

from soc_assets.models import TermGroup


class TermGroupList(APIView):
    """ 单位
    """

    def get(self, request):
        """ 单位
        """
        list = TermGroup.objects.all().values('term_group_id', 'term_group_name')
        result = []
        for item in list:
            result.append({
                'id': item['term_group_id'],
                'name': item['term_group_name']
            })
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)
