from django.shortcuts import render , redirect , get_object_or_404
from django.http import JsonResponse
from.models import Like,Video,Category
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView
from .mixins import LoginRequire
from django.db.models import Q
from django.views.generic import ListView,CreateView
def home(request):
    recent_videos = Video.objects.published().order_by('-date')[:6]
    popular_posts= Video.objects.published().order_by('-hit_count_generic__hits')[:6]
    return render(request,"home/index.html",{"recent_videos":recent_videos ,'popular_posts':popular_posts })

class VideoDetailView(HitCountDetailView,LoginRequire):
    model = Video
    template_name = 'home/video-detail.html'
    context_object_name = 'video'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.likes.filter(video__slug=self.object.slug,user_id=self.request.user.id).exists():
            context["liked"]=True
        else:
            context["liked"]=False
        return context

   


class CategoryList(ListView):
    paginate_by = 6
    template_name = "video/all-videos.html"
    context_object_name="video"
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.posts.published()

def search(request):
    search=request.GET.get('q')
    posts=Video.objects.published().filter(Q(description__icontains=search) | Q(title__icontains=search))
    paginator= Paginator(posts,6)
    page_number=request.GET.get('page')
    objects_list=paginator.get_page(page_number)
    return render(request , "video/search.html" ,{'video':objects_list})



def like(request,slug,pk):
    if request.user.is_authenticated:
        try:
            like=Like.objects.get(video__slug=slug,user_id=request.user.id)
            like.delete()
            return JsonResponse({"response":"unliked"})
        except:
            Like.objects.create(video_id=pk,user_id=request.user.id)
            return JsonResponse({"response":"liked"})
    else:
        return redirect("accounts:login")

def likes(request):
    like=Like.objects.filter(user_id=request.user.id)
    return render(request,"home/likes.html",{"likes":like})
#-----------------------------------------------------------------------------------------------------------




