from django.utils.translation import gettext_lazy as _

MR = 'MR'
MRS = 'MRS'
MISS = 'MISS'
OTHERS = 'OTHERS'

TITLE_CHOICES = [
    (MR, _('Mr')),
    (MRS, _('Mrs')),
    (MISS, _('Miss')),
    (OTHERS, _('Others')),
]
