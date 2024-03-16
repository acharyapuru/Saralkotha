from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserProfile,ReportPost
from .utils import send_mail_to_admin


@receiver(post_save,sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            name = instance.name,
            email = instance.email,
            phone=instance.phone
        )






@receiver(post_save,sender=ReportPost)
def check_report_count(sender, instance, **kwargs):
    report_count = ReportPost.objects.filter(post=instance.post).count()
    if report_count>=4:
        instance.post.availability = False
        instance.post.save()
        send_mail_to_admin(instance.post)
