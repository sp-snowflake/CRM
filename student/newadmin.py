from newadmin.sites import site
from student import models

# print('student admin------------')

class TestAdmin(object):
    list_display = ['name']

site.register(models.Test,TestAdmin)


