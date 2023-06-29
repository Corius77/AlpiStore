from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=200, null=False)
    topic = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False)
    message = models.TextField(max_length=200, null=False)

    def __str__(self):
        return self.topic
