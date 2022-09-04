from django.urls import path
from django.contrib.auth import views as view
from . import views
app_name="accounts"

urlpatterns=[ 
    path("register",views.UserRegister.as_view(),name="register"),
    path("logout" , views.user_logout , name = "logout"),
    path("login" ,views.UserLogin.as_view() , name = "login" ),
    path("user/panel" ,views.user_info , name = "userpanel" ),
    path("profile/" , views.EditProfileView.as_view() , name = "edit"),
    path("activate/<uidb64>/<token>",views.activate,name='activate'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('teacher/profile', views.Profile.as_view(), name="profile"),
] 

 
