from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #We can get one and only one blog post by using pk
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST) #If method is POST then we want to construct the PostForm with data from the form
        if form.is_valid(): #if the form is correct (all required fields are set and no incorrect values have been submitted).
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            '''
            Basically, we have two things here: we save the form with form.save and we add an author (since there was 
            no author field in the PostForm and this field is required). commit=False means that we don't want to save 
            the Post model yet – we want to add the author first. Most of the time you will use form.save() without 
            commit=False, but in this case, we need to supply it. post.save() will preserve changes (adding the author) 
            and a new blog post is created!
            '''
            return redirect('post_detail', pk=post.pk) # will redirect to post_detail page newly created post
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


'''
To create a new Post form, we need to call PostForm()
'''

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html',{'form':form})

'''
when we create a form, we pass this post as an instance, both when we save the form…

    form = PostForm(request.POST, instance=post)
…and when we've just opened a form with this post to edit:


    form = PostForm(instance=post)
'''