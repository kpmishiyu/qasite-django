from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('ask/', views.ask_question, name='ask_question'),
    path('signup/', views.signup, name='signup'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer/<int:pk>/accept/', views.accept_answer, name='accept_answer'),
    path('my-profile/', views.my_profile, name='my_profile'),
]