from django.shortcuts import render
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from .mixins import SuperUserAccessMixin,AuthorAccessMixin,FormValidMixin,FieldsMixin
from home.models import Video
from django.urls import reverse_lazy
from accounts.models import Notification
from django.http import JsonResponse
class AllVideos(ListView):
    context_object_name= "video"
    template_name= "video/all-videos.html"
    paginate_by= 3
    def get_queryset(self):
        return Video.objects.published()

class AllVideosHitCount(ListView):
    context_object_name= "video"
    template_name="video/all-videos-hit-count.html"
    paginate_by=3
    def get_queryset(self):
        return Video.objects.published().order_by('-hit_count_generic__hits')[:6]

class VideoList(ListView):
    template_name="registration/home.html"

    def get_queryset(self):
        if self.request.user.is_admin:
            return Video.objects.all()
        else:
            return Video.objects.filter(auther=self.request.user)

class VideoCreate(FormValidMixin,FieldsMixin,CreateView):
    model=Video
    fields=['auther','category','title','description','time','video','image','publish','status','slug']
    template_name="registration/article-create-update.html"
    success_url=reverse_lazy("video:VideoList")

class VideoUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Video
    template_name = "registration/article-create-update.html"
    success_url=reverse_lazy("video:VideoList")


class VideoDelete(SuperUserAccessMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('accounts:profile')
    template_name = "registration/article_confirm_delete.html"

def delete_notification(request,pk):
    notif=Notification.objects.get(id=pk)
    notif.delete()
    return JsonResponse({"response":"deleted"})