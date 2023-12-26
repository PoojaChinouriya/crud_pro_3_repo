from django.urls import path
from .views import PersonDetail, PersonAPI

urlpatterns = [
    path('personApi/', PersonAPI.as_view()),
    path('person-retrive/<int:pk>/',PersonDetail.as_view()),
]
