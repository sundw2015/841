# # coding: utf-8
# from common import notify_administrator
# from celery.task import task
#
#
# @task(bind=True)
# def notify_admin(self, msg, title):
#     """
#     通知管理员
#     :param msg:
#     :param title:
#     :return:
#     """
#     notify_administrator(content=msg, title=title)
