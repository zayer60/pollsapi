from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('polls',PollViewSet,basename='polls')

urlpatterns = [
    path('polls/<int:pk>/choices/',ChoiceListAPI.as_view(),name='choice_list'),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/",CreateVote.as_view(),name='create_vote'),
    path('user/',CreateUser.as_view(),name='create_user'),
    path('login/',LoginView.as_view(),name='login'),
]

urlpatterns += router.urls