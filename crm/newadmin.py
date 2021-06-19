from newadmin.sites import site
from crm import models
from newadmin.admin_base import BaseNewAdmin

# print('newadmin-----------')

class CustomerAdmin(BaseNewAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']    # 外键关联的表，要写清楚搜索哪个字段
    readonly_fields = ['status','contact']
    filter_horizontal = ['consult_cources',]

site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.Role)
site.register(models.Menus)
site.register(models.UserProfile)
