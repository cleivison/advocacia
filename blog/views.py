from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post,Tag
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from blog.utils import GenericPaginator
from django.views import generic
def post_list(request):
    tags = Tag.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 4)  # mostrar ate 25 posts por page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog.html', {'posts': posts,'tags':tags})

def list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'lista_de_post.html',{'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = Tag.objects.all()
    return render(request, 'post_detalhe.html', {'post': post,'tags':tags})


@login_required(login_url='/usuario/login/')
@permission_required('request.user.is_superuser', login_url='/usuario/login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("/blog/")
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
    
@permission_required('request.user.is_superuser', login_url='/usuario/login/')
def new_tag(request):
    form = TagForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('post_new')
    return render(request,'post_edit.html',{'tag':form})

   
@login_required(login_url='/usuario/login/')
@permission_required('request.user.is_superuser', login_url='/usuario/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/blog/')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required(login_url='/usuario/login/')
def excluir_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect("/blog/all/posts/")

class TagPostsView(generic.ListView):
    template_name = 'blog_posts_tag.html'
    paginate_by = 4

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        results_filter = Post.objects.filter(
            tags=self.tag
        ).order_by('-created_date').order_by('-id')
        return results_filter

    def get_context_data(self, **kwargs):
        context_data = super(TagPostsView, self).get_context_data(**kwargs)
        context_data['tag'] = self.tag
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data