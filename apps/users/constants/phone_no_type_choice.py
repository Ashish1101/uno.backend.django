from django.utils.translation import gettext_lazy as _

MOBILE = 'MOBILE'
OFFICE = 'OFFICE'
RESIDENCE = 'RESIDENCE'

PHONE_NO_TYPE_CHOICES = [
    (MOBILE, _('Mobile')),
    (OFFICE, _('Office')),
    (RESIDENCE, _('Residence')),
]
