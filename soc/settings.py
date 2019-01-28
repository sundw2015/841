# coding=utf8
"""
Django settings for soc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# login salt
LOGIN_SALT = 'i480g1972nJh036HU3gD8Jbg5EGgLasdkk7PYzNX6e8ud49By5fnL6ZW7IZ6Zoqh'
EMAIL_SALT = 'jGXsPQ3MvlmTwr1qQ5f3gK68bb3x04p0353HY0mdY520tx3l3mFg50Bu2L842h0I'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djcelery',
    'rest_framework',
    'rest_framework.authtoken',
    'soc',
    'soc_user',
    'soc_datatable',
    'soc_system',
    'soc_ssa',
    'soc_knowledge',
    'soc_demodata',
    'soc_assets',
    'soc_scan',
    'soc_task'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.DisableCsrf',
    'soc.middleware.BlackIP',
    'soc.middleware.Permission',
    'soc.middleware.SocLog',
    'soc.middleware.NodeAPIProxy',
)

# 自定义模块不能编译
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'utils.backends.EmailAuthBackend',
)

# amdins
ADMINS = ()

ROOT_URLCONF = 'soc.urls'

WSGI_APPLICATION = 'soc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'soc',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# DATABASE_ROUTERS = ['soc.admin.AuthRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    os.path.join(SITE_ROOT, 'templates'),
)

# media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

MEDIA_DIRS = (
    ("images", os.path.join(MEDIA_ROOT, 'images')),
    ("js", os.path.join(MEDIA_ROOT, 'js')),
    ("css", os.path.join(MEDIA_ROOT, 'css'))
)

# Template dir
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Fixtures dir
FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures')]

# logging
LOGGING = json.load(open(os.path.join(BASE_DIR, "soc/log_config.json"), 'r'))

DOWNLOAD_DIR = os.path.join('media', 'download')
CSV_TEMPLATE = os.path.join('media', 'csv_template')
AVATAR_DIR = os.path.join('media', 'avatar')
REPORT_DIR = os.path.join('media', 'reports')
TICKET_ATTACHMENT_DIR = os.path.join('media', 'ticket_attach')
SCREENSHOT_DIR = os.path.join('media', 'screenshots')
PCAP_DIR = os.path.join('media', 'pcap')
PDF_DIR = os.path.join('media', 'pdf')

# EMAIL CONFIG
EMAIL_HOST_USER = 'alarm@qssec.com'
EMAIL_HOST_PASSWORD = 'qssec2014'
EMAIL_HOST = 'smtp.exmail.qq.com'
SERVER_EMAIL = 'alarm@qssec.com'

# 短信用户密码
SEND_PHONE_MESSAGE_URL = ''
CORP_ID = ''
CORP_PWD = ''

# arachni 扫描单个页面超时时间
ARACHNI_SCAN_PAGE_TIMEOUT = 60 * 60

# redis server address
BROKER_URL = 'redis://localhost:6379/0'
# store task results in redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# task result life time until they will be deleted
CELERY_TASK_RESULT_EXPIRES = 7 * 86400  # 7 days
# needed for worker monitoring
CELERY_SEND_EVENTS = True
# where to store periodic tasks (needed for scheduler)
# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
#
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

AGENT_SECRET_KEY = ''

# 执行层操作机器的超时时间
EXECUTE_TELNET_TIMEOUT = 0.1
EXECUTE_HTTPS_TIMEOUT = 10
EXECUTE_SSH_TIMEOUT = 1

HEARTBEAT_KEY = ''

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 直接调用接口返回json数据格式,而不是 BrowsableAPI 格式, 防止暴露借口文档
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        # 联系我们接口, 3次/min
        'contact_us': '3/m',
        # 短信验证， 2次/min
        'phone_captcha': '2/m',
        # 邮件验证，找回密码 2次/m
        'email_verification': '2/m',
        # 高防数据接口
        'hw_data': '15/m',
        # 获取中心节点 auth_key
        'get_auth_key': '5/m',
    },
    'EXCEPTION_HANDLER': 'utils.handlers.custom_exception_handler',
}
# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# 文件上传处理
FILE_UPLOAD_HANDLERS = (
    "utils.handlers.ProgressFileUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
)

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    'api_path': '/',
    "api_version": '0.1.10',  # Specify your API's version (optional)
    "token_type": 'Bearer',
    "enabled_methods": [  # Methods to enable in UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "is_authenticated": False,
    'doc_expansion': 'list',
}

# Provider that shows on the Google Authenticator
QSSEC_SOC = "Yunsong"

# HADES SECURITY KEY
HADES_SECURITY_KEY = ""

# Notifications

ENV = ""

NOTIFY_WORKER_ORDER_EMAIL = ('qiuwh@qssec.com', 'wuzx@qssec.com', 'guoyang@qssec.com',)

ASIC_ERROR_EMAIL = ('liupeng@qssec.com', 'fanyb@qssec.com', 'wuzx@qssec.com',)

ADMINISTRATORS = ('qiuwh@qssec.com', 'wuzx@qssec.com', 'guoyang@qssec.com',)

ELASTICSEARCH_HOSTS = ['http://127.0.0.1:9200/']
# SSA_ELASTICSEARCH_HOSTS = ["http://39.104.91.84:9200/"]

# NIDS 配置redis
NIDPS_REDIS_HOST = '127.0.0.1'
NIDPS_REDIS_DB = 0
NIDPS_REDIS_PORT = 6379
NIDPS_REDIS_PASSWORD = None

# 系统资源 redis
SYS_REDIS_HOST = '127.0.0.1'
SYS_REDIS_DB = 1
SYS_REDIS_PORT = 6379
SYS_REDIS_PASSWORD = None

# 检查备案
QUERY_DOMAIN_ICP_URL = ''
QUERY_DOMAIN_USER = ''
QUERY_DOMAIN_PASSWORD = ''

# session 过期时间, 24*3小时,
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 86400 * 3
# 两次request时间为15分钟，超时自动登出(配置在代理商级别，之后可以修改)
# LOGIN_TIMEOUT = 15*60

# sohu email
SOHU_EMAIL_URL = ''
SOHU_EMAIL_API_USER = ''
SOHU_EMAIL_API_KEY = ''

# 合作联系人
SALESMANS = []

SSO_PRIVATE_KEY = ""

# IDPS 申请联系人
IDPS_ADMINS = []

WY_RSA_PUB = "wy_rsa_pub"
# 私有化代理商信息
AGENT = {
    "phone": "(暂无)"
}

# kafak地址
KAFAK_HOST = '39.104.86.160:9092'

# 事件ES
EVENT_ELASTICSEARCH_HOSTS = ["http://127.0.0.1:9200/"]
EVENT_TOKEN = "705fea8d42471a7c0977734089e2f200"
EVENT_REPORT_URL = "http://127.0.0.1:80/api/accept_event"

TARGET_LOCATION = ""
SSA_COMPANY = ""

try:
    from local_settings import *
except ImportError:
    print("local_settings not found, run at default settings")

# 邮件头
from init import VERSION

v = "v" + '.'.join(str(x) for x in VERSION[:3])
EMAIL_SUBJECT_PREFIX = '[Yunsong {0} {1}]'.format(ENV, v)

print(EMAIL_SUBJECT_PREFIX)

# celery
# import djcelery

# djcelery.setup_loader()
