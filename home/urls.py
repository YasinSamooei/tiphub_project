from django.urls import path,re_path,include
from . import views

app_name="home"
urlpatterns=[
    path("",views.home,name="MainPage"),
    re_path(r'video/detail/(?P<slug>[-\w]+)',views.VideoDetailView.as_view(),name="videodetail"),
    re_path(r'category/(?P<slug>[-\w]+)',views.CategoryList.as_view(),name="category_detail"),
    path("search" , views.search , name = "search"),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    re_path(r"like/(?P<slug>[-\w]+)/(?P<pk>[-\w]+)",views.like,name="like"),
    path("like",views.likes,name="likes"),
]
