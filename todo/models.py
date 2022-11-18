from django.db import models

# Create your models here.
class TodoList(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    userid = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title