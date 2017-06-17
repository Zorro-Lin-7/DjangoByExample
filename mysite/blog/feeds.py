from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
    #RSS elements
    title = "My blog"
    link = '/blog/'
    description = 'New posts of my blog.'
    
    # retrieves the objects to be included in the feed
    def items(self):  			
        return Post.published.all()[:5]
        
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return truncatewords(item.body, 30)