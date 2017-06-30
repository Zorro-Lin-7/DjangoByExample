from django.db import models
from django.conf import settings
from django.utils.text import slugify
# the model we are going to use to store images bookmarked from different sites.
class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField
    image = models.ImagedField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,db_index=True)
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image, self).save(*args, **kwargs)