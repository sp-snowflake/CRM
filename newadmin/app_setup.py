from django import conf



def newadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.newadmin' % app_name)
            print(mod.newadmin)
        except ImportError:
            pass












