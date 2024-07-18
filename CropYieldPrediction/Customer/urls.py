from django.urls import path
from .import views

urlpatterns=[
    path('index',views.index,name='homepage'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('crop',views.crop_data,name='crop'),
    path('predict',views.predict,name='predict')
]