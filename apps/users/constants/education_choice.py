from django.utils.translation import gettext_lazy as _

BELOW_SSC = 'BELOW SSC'
SSC = 'SSC'
HSC = 'HSC'
GRADUATE = 'GRADUATE'
POST_GRADUATE = 'POST-GRADUATE'
PROFESSIONAL = 'PROFESSIONAL'

EDUCATION_CHOICES = [
    (BELOW_SSC, _('Below SSC')),
    (SSC, _('SSC')),
    (HSC, _('HSC')),
    (GRADUATE, _('Graduate')),
    (POST_GRADUATE, _('Post-Graduate')),
    (PROFESSIONAL, _('Professional')),
]
