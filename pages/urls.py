from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about , name="about"),
    path('contact/',views.contact , name="contact"),
    path('princing/',views.pricing , name="pricing"),
    path('studentdashbord/',views.studentdashbord , name="studentdashbord"),
    path('professordashbord/',views.professordashbord , name="professordashbord"),
    path('studentdashbord/studentedit',views.studentedit , name="studentedit"),
    path('signin/',views.signin , name="signin"),
    path('signup/',views.signup , name="signup"),
    path('logout/', views.logout_view, name='logout'),
]