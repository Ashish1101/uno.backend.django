from django.utils.translation import gettext_lazy as _

GENERAL = 'GENERAL'
OBC = 'OBC'
SC = 'SC'
ST = 'ST'
OTHERS = 'OTHERS'

CATEGORY_CHOICES = [
    (GENERAL, _('General')),
    (OBC, _('OBC')),
    (SC, _('SC')),
    (ST, _('ST')),
    (OTHERS, _('Others')),
]
