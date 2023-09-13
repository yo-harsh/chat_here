from django.db import models

# Create your models here.


class PdfFiles(models.Model):
    file = models.FileField(upload_to='store/pdf/')

    def __str__(self):
        return str(self.file) # Ensure pdf is converted to a string

