from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Content(models.Model):
    usr = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, blank=False)
    category = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    filename = models.FileField(upload_to='photos/')
    downloaded = models.IntegerField(default=0)
    @property
    def filename_url(self):
        if self.filename and hasattr(self.filename, 'url'):
            filen = self.filename.url
            print(filen)
            return  filen

    def update_dwnlds(self):
            dwncount = self.downloaded
            print("dwncount = ")
            print(dwncount)
            self.downloaded =  dwncount + 1
            print("self.downloaded = ")
            print(self.downloaded)
            self.save()
    def savecontent(self, usr):
            self.usr = usr
            self.save()

class CellNo(models.Model):
      usr = models.ForeignKey('auth.User',  on_delete=models.CASCADE)
      number = models.IntegerField()
      def __str__(self):
         return self.number

class Downloads(models.Model):
    usr = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contnt = models.ForeignKey('pique.Content', on_delete=models.CASCADE)
    download_date = models.DateTimeField(default=timezone.now)
# Create your models here.
