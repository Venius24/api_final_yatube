from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Регистрируем ваш ViewSet. 'posts' — это префикс в URL
router.register('posts', views.PostViewSet, basename='post')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)
router.register('follow', views.FollowViewSet, basename='follow')
router.register('groups', views.GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
