from django.db import models

# Create your models here.

class Organization(models.Model):
    name = models.CharField(verbose_name="organization name", max_length=200)
    creator_id = models.BigIntegerField(verbose_name="create")

    def toJson(self):
        return {
            "pk" : self.pk,
            "name" : self.name,
            "creator" : self.creator_id
        }
    
    def __str__(self):
        return f"{self.pk}. {self.name}"