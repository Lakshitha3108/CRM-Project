from django.db import models

# Create your models here.

from students.models import BaseClass

class Courses(BaseClass):

    name = models.CharField(max_length=50)

    photo = models.ImageField(upload_to='courses')

    duration = models.CharField(max_length=25)

    code = models.CharField(max_length=15)

    fee = models.FloatField()

    offer_fee = models.FloatField(null=True,blank=True)

    def __str__(self):

        return f'{self.code}'
    
    class Meta:

        verbose_name = 'Courses'

        verbose_name_plural ='Courses'