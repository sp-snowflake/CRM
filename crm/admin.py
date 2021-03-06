from django.contrib import admin
from crm import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']    # 外键关联的表，要写清楚搜索哪个字段



admin.site.register(models.CustomerInfo,CustomerAdmin)
admin.site.register(models.CustomerFollowup)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Student)
admin.site.register(models.UserProfile)

