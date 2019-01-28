# coding=utf-8
from django.conf.urls import patterns, url
from soc_assets import views

urlpatterns = patterns(
    '',
    # 单位
    url(r'^team/list$', views.TermGroupList.as_view()),
)
