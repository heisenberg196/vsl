from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class vidFile(models.Model):
    file = models.FileField(_("Video File"), upload_to='traffic-feed')
    location = models.CharField(max_length=128, blank=True, null=True)
    
