from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


# db & admin pannel validator
def validate_phone(value):
    reg = re.compile(r"^(01[0|1|6|7|8|9])\d{7,8}$")
    if not reg.match(value):
        raise ValidationError("유효성 검사에 위배 됩니다")
        # raise ValidationError(_("%(value) 지원되지 않는 형식입니다."), params={"value": value})
