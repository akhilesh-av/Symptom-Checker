from django.db import models


class Chat(models.Model):
    text = models.CharField(max_length=300)
    
    def __str__(self):
        return str(self.text)