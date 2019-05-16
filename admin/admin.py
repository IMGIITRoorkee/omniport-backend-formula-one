from formula_one.models import (
    ContactInformation,
    LocationInformation,
    SocialInformation,
    SocialLink,
)
from omniport.admin.site import omnipotence

# Register all non-swappable models

omnipotence.register(ContactInformation)
omnipotence.register(LocationInformation)
omnipotence.register(SocialInformation)
omnipotence.register(SocialLink)
