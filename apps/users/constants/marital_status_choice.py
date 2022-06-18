from django.utils.translation import gettext_lazy as _

MARRIED = 'MARRIED'
WIDOWED = 'WIDOWED'
DIVORCED_OR_SEPARATED = 'DIVORCED OR SEPARATED'
NEVER_MARRIED_OR_SINGLE = 'NEVER MARRIED OR SINGLE'

MARITAL_STATUS_CHOICES = [
    (MARRIED, _('Married')),
    (WIDOWED, _('Widowed')),
    (DIVORCED_OR_SEPARATED, _('Divorced or Separated')),
    (NEVER_MARRIED_OR_SINGLE, _('Never Married or Single')),
]
