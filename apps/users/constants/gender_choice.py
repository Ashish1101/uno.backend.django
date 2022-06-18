from django.utils.translation import gettext_lazy as _

MALE = 'MALE'
FEMALE = 'FEMALE'
OTHERS = 'OTHERS'

GENDER_CHOICES = [
    (MALE, _('Male')),
    (FEMALE, _('Female')),
    (OTHERS, _('Others')),
]

