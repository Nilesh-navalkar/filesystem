from django.db import models
# Create your models here.
class folders(models.Model):
    foldername=models.TextField()
    email=models.EmailField()
    parent=models.TextField(default='')
    def __str__(self):
        return self.email+'/'+self.foldername

class files(models.Model):
    filename=models.TextField()
    foldername=models.TextField()
    email=models.EmailField()
    file=models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.email+'/'+self.foldername+'/'+self.filename
