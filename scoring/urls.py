from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import ScoresViewSet

router = DefaultRouter()
router.register(r'', ScoresViewSet, basename='scores')
urlpatterns = [
    url(r'^', include(router.urls))
]