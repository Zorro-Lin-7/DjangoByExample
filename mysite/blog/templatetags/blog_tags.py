from django import tempalte

register = tempalte.Library()

from .. models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()