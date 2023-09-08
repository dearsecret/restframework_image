import requests
from .signature import sms


def send_sms(to: str, content: str):
    # SMS bytes 크기 90으로 제한된다.
    if len(content.encode()) < 90:
        try:
            res = requests.post(**sms(to, content))
            return res
        except Exception as e:
            content = f"{e}"
        # finally :
        #     SMSMessage.objects.create(to=to, content=content)


# from django.core.mail import send_mail
# from django.utils.html import strip_tags
# from django.template.loader import render_to_string
# from config import settings
# def send_email(to: list, subject: str, template_name: str, **context):
#     # verify.html examples
#     # context = {
#     #     "title" : title,
#     #     "subtitle" : subtitle,
#     #     "content" : RandomNumber,
#     #     "anotation" : "blabla",
#     # }
#     try:
#         html_msg = render_to_string(template_name=template_name, context=context)
#         plain_txt = strip_tags(html_msg)
#         send_mail(
#             subject,
#             plain_txt,
#             settings.DEFAULT_FROM_EMAIL,
#             to,
#             html_message=html_msg,
#         )
#     except Exception as e:
#         plain_txt = f"{e}"

#     # finally :
#     #     for user in to :
#     #         Mail.objects.create(to=user, subject=subject, content=plain_txt)
