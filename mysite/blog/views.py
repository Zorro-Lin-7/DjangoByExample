from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

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
                                   
    return render(request,'blog/post/detail.html',{'post':post})

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
    
    if request.method == 'POST':      # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():           # Form fields passed validation
            cd = form.cleaned_data    # ...send email    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})
                                                    
                                                             