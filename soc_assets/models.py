# coding=utf-8
from django.db import models

# Create your models here.


class Assets(models.Model):
    ip = models.CharField(max_length=64)
    assets_name = models.CharField(max_length=200)
    add_date = models.DateTimeField(null=True, blank=True)
    last_date = models.DateTimeField(null=True, blank=True)
    assets_type = models.IntegerField()
    term_group_id = models.CharField(max_length=64, default='0')
    term_duty = models.CharField(max_length=64, default='0')

    class Meta:
        db_table = "soc_assets"


class AssetsType(models.Model):
    assets_type_name = models.CharField(max_length=64)

    class Meta:
        db_table = "soc_assets_type"


class TermGroup(models.Model):
    # 部门ID
    term_group_id = models.CharField(max_length=64, default=0)
    # 部门名称
    term_group_name = models.CharField(max_length=200)

    class Meta:
        db_table = "soc_term_group"


