from random import random
from django.db import models
from django.utils import timezone
from .validators import validate_phone
from .messages import send_sms
from common.models import CommonModel

# Create your models here.


class Number(CommonModel):
    user = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    number = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_phone],
    )

    def tried(self):
        return f"{self.messages.count()}"

    def __str__(self):
        return f"{self.number}"


class VerifyNumber(models.Model):
    number = models.ForeignKey(
        Number, related_name="messages", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=6, editable=False)
    sended = models.BooleanField(default=False, editable=False)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sended:
            before_date = timezone.localtime(
                timezone.now() - timezone.timedelta(days=1)
            )
            if VerifyNumber.objects.filter(time__gte=before_date).count() < 500:
                self.content = str(random())[-1:-7:-1]
                message = f"APPNAME [{self.content}] 인증번호를 입력하세요."
                result = send_sms(self.number.number, message)
                if result.status_code == 202:
                    self.sended = True
        super(VerifyNumber, self).save(*args, **kwargs)
