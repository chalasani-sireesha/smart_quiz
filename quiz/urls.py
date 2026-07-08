from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name = "home"),
    path("quiz/<int:quiz_id>/",views.quiz_detail,name="quiz_detail"),
    path("result/",views.result,name="result"),
    path("leaderboard/",views.leaderboard,name="leaderboard"),
    path("certificate/",views.download_certificate,name="download_certificate"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact")
    
]