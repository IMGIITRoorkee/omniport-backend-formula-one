from formula_one.models import (
    ContactInformation,
    LocationInformation,
    SocialInformation,
    SocialLink,
)
from formula_one.forms.admin import admin_form_dict
from omniport.admin.site import omnipotence

# Register all non-swappable models

omnipotence.register(ContactInformation, admin_form_dict['ContactInformation'])
omnipotence.register(
    LocationInformation,
    admin_form_dict['LocationInformation'],
)
omnipotence.register(SocialInformation, admin_form_dict['SocialInformation'])
omnipotence.register(SocialLink)
