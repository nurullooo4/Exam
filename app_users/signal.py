# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings
#
# from app_users.models import UserModel
#
#
# @receiver(signal=post_save, sender=User)
# def profile_create_on_user_create(sender, instance, created, **kwargs):
#     if created:
#         profile = UserModel.objects.create(
#             user=instance,
#             fullname=f'{instance.first_name} {instance.last_name}' if instance.first_name.strip() and instance.last_name else '',
#             email=instance.email,
#         )
#         profile.save()
#
#         subject = 'Welcome to Online Store !'
#         message = 'We are glad to see you there'
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[instance.email],
#             fail_silently=True,
#         )
