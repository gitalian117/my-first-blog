from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
#           post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


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
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


""""
def post_draft_list(request):
    posts = Post.objects.filter(published_date_isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts:': posts})
"""

"""
Postはクラス、requestとpkに対応したインスタンス＝投稿を返す。pkはurlsの中で定義されていて、このviewsを参照するように定義つけてれている。
1個目のifの意味はリクエストに対して要求されてるのがPOST関数の場合、つまりなんらかの編集を加えて”送信している場合”にこっちの条件分岐に飛ぶってこと。
2個目のifは純粋にエラーじゃないかを確認してる（投稿の値が正常か。（空のまま送信してきたりしてないかとか））
で、elseは送信とかじゃない場合。
ちなみに
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'title', 'text',}
ていうクラス。
で、ModelFormはその名の通りモデルからフォームを作成する。つまり本来フォームを作るときにはフィールドの定義が必要やけど、すでに入れたいモデルが定義されてる場合、それをそのまま入れましょうっていう関数。今回は下につけてモデルはPostって入れてる。

"""




    
