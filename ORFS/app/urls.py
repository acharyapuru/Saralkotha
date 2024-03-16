from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('login/',views.Log_in,name='login'),
    path('signup/',views.Sign_up,name='signup'),
    path('profile/<int:pk>/',views.ProfileView.as_view(),name='profile'),
    path('login/',views.Log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('passwordchange/',views.Password_chage,name='passwordchange'),
    path('passwordreset/',views.Password_set,name='password_reset'),
    path('userdetail/<int:id>/',views.user_detail,name='userdetail'),

    path('create/',views.PostCreateView.as_view(),name='create-post',),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/report/',views.ReportView.as_view(),name='report'),
    path('findnearby/',views.FindNearByView.as_view(),name='find_nearby')
    
]
