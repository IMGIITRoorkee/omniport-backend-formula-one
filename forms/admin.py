from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import ModelForm

from formula_one.models import (
    ContactInformation,
    LocationInformation,
    SocialInformation,
)

admin_form_dict = {
    'ContactInformation': ContactInformation,
    'LocationInformation': LocationInformation,
    'SocialInformation': SocialInformation,
}

def return_admin_form(class_name):
    """
    """

    class Form(ModelForm):
        """
        """

        entity_content_object = forms.CharField(widget=forms.Select)

        def __init__(self, *args, **kwargs):
            super(Form, self).__init__(*args, **kwargs)
   
        def save(self, *args, **kwargs):
            self.instance.entity_object_id = (
                self.cleaned_data['entity_content_object']
            )
            return super(Form, self).save(*args, **kwargs)
        
        class Meta:
            model = admin_form_dict[class_name]
            fields = '__all__'


    class FormAdmin(ModelAdmin):
        """
        """

        form = Form
        exclude = ['entity_object_id']
    
    return FormAdmin

for key in admin_form_dict:
    admin_form_dict[key] = return_admin_form(key)
