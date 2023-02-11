from django.db import models

# Create your models here.
class mashup_data(models.Model):
    singername=models.CharField(max_length=1000)
    n_videos=models.PositiveIntegerField()
    duration=models.PositiveIntegerField()
    email=models.EmailField()

    def __str__(self):
        return self.email
