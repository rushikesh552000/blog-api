from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostModel
from django.core.mail import EmailMessage
from django.conf import settings

@receiver(post_save, sender=PostModel)
def handle_post_model_saved(sender, instance, created, **kwargs):
    if created:
        mail_subject = f'Verify Account'
        to_email = instance.author.email
        from_email = settings.SENT_FROM_EMAIL
        message = f'''Post is created with title {instance.title} and body {instance.body}'''
        email = EmailMessage(mail_subject, message, from_email, [to_email])
        email.content_subtype = "html"
        email.send()
