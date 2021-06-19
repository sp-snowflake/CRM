
from django.forms import ModelForm


def create_dynamic_model_form(admin_class,form_add=False):
    """动态的生成modelform
    form_add : False默认是修改的表单，True时为添加
    """
    class Meta:
        model = admin_class.model
        # fields = ['name','consultant','status']
        fields = "__all__"
        if not form_add:
            exclude = admin_class.readonly_fields
            admin_class.form_add = False # 这是因为自始至终admin_class实例都是同一个，
                                    # 这里修改属性为True是为了避免上一次添加调用将其改为了True
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled':'true'})
            #     # cls.Meta.exclude.append(field_name)
        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm",(ModelForm,),{'Meta':Meta,'__new__':__new__})
    return dynamic_form


