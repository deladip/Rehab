from django.urls import path
from . import views

urlpatterns = [

    path('main/', views.mainPage),    
    path('index/', views.index, name='index'),
    path('privacy/', views.privacy, name='privacy'),

    path('register/', views.registerPage,name='register'),
    path('login/', views.empLogin, name='login'),
     path('logout/', views.logoutUser, name='logout'),

    path('home/', views.home, name= 'home'),
    path('user/', views.userPage, name= 'user'),    
   
    path('account/', views.accountSettings, name= 'account'),   
    

    path('patient/',views.patient, name='patient'),
    path('profile/<str:pk_test>/', views.ptprofile, name='profile'),

    path('schedule/<str:pk>/', views.schedule, name='schedule'),
    path('update_schedule/<str:pk>/', views.updateSchedule, name='update_schedule'),
    path('delete_schedule/<str:pk>/',views.deleteOrder, name='delete_schedule'),

]