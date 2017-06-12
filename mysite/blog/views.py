from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
#def post_list(request):
#    posts = Post.published.all()
#    return render(request,
#                  'blog/post/list.html',
#                  {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # Chapter 2                               
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':     # A comment was posted
        comment_form = CommentForm(data=request.POST)
     
        if comment_form.is_valid():  
            new_comment = comment_form.save(commit=False)  # Create Comment object but don't save to database yet
            new_comment.post = post    # Assign the current post to the comment
            new_comment.save()         # Save the comment to the database
    else:
        comment_form = CommentForm()
        
    # List of similar posts
    post_tags_ids = post.tags.values_list('id',falt=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4]
                                                                                                        
    return render(request,'blog/post/detail.html',{'post':post,
                                                   'comments': comments,
                                                   'comment_form': comment_form})

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts':posts})
                   
# This class-based view is analogous to the previous post_list view.                   
class PostListView(ListView):
    queryset = Post.published.all() #Use a specific QuerySet 【attribute】 instead of retrieving all objects
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'     
    
    
#Chapter 2

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':      # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():           # Form fields passed validation
            cd = form.cleaned_data    
            # ...send email  
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'admin@myblog.com',[cd['to']])
            sent = True  
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
                                                   