from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PostModel(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    is_show = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    # def save_model_and_trigger_signal(self):
    #     # Save your machine learning model here
    #
    #     # Trigger the signal
    #     model_saved_signal.send(sender=self.__class__)