from newadmin.admin_base import BaseNewAdmin


class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}

    def register(self,model_class,admin_class=BaseNewAdmin):
        """注册admin表"""

        print('register',model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name

        if not admin_class:     # 为了避免多个model共享同一个BaseNewAdmin内存对象
            admin_class = BaseNewAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class
        if app_name not in site.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class


site = AdminSite()






