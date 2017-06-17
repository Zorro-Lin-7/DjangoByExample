from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap): # inheriting the Sitemap class of the sitemaps module.
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):  #receives each object returned by items() 
        return obj.publish   # returns the last time the object was modi ed. 