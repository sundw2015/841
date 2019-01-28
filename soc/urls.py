# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from soc import views
from settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

api_urlpatterns = patterns('',
                           # Examples:
                           url(r'^', include('soc_user.urls')),
                           # 系统设置
                           url(r'^system/', include('soc_system.urls')),
                           # 系统升级
                           url(r'^upgrade$', views.Upgrade.as_view()),
                           url(r'^permission$', views.RolePermissionList.as_view()),
                           url(r'^permission/list$', views.RolePermissionSelectList.as_view()),
                           url(r'^permission/(?P<role_id>\d+)$', views.RolePermissionDetail.as_view()),
                           url(r'^role/dts$', views.RoleList.as_view()),

                           # 安全态势感知(Security Situation Awareness)
                           url(r'^ssa/', include('soc_ssa.urls')),
                           # 安全运维管理知识库
                           url(r'^op_store/', include('soc_knowledge.urls')),

                           # 资产
                           url(r'^assets/', include('soc_assets.urls')),
                           # 扫描
                           url(r'^scan/', include('soc_scan.urls'))
                           )

urlpatterns = patterns('',
                       url(r'^api/', include(api_urlpatterns)),
                       )
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^api/docs/', include('rest_framework_swagger.urls'))]
    urlpatterns += [url(r'^admin/', include(admin.site.urls))]
