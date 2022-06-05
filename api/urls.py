from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import TopicsViewSet, StudentsViewSet, QuestionsViewSet, enroll_topic, evaluate_answers
from django.urls import path

router = DefaultRouter()
router.register(r'topic', TopicsViewSet, basename='topics')
router.register(r'student', StudentsViewSet, basename='students')
router.register(r'question', QuestionsViewSet, basename='question')


urlpatterns = [
    url(r'^', include(router.urls)),
    path('enroll/', enroll_topic),
    path('evaluate/', evaluate_answers)
]