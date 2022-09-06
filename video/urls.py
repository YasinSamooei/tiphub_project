from django.urls import path
from . import views

app_name="video"

urlpatterns=[
    path("",views.AllVideos.as_view(),name="AllVideos"),
    path("hit/count",views.AllVideosHitCount.as_view(),name="all-videos-hit-count"),
    path("list",views.VideoList.as_view(),name="VideoList"),
    path("create",views.VideoCreate.as_view(),name="video-create"),
    path('update/<int:pk>', views.VideoUpdate.as_view(), name="video-update"),
    path('delete/<int:pk>', views.VideoDelete.as_view(), name="video-delete"),
    path('delete/notif/<int:pk>',views.delete_notification,name="delete-notif"),
]