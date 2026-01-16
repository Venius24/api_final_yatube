from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group


User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['post', 'author']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
        read_only_fields = ['user']
    
    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        
        # 1. Проверка на самого себя
        if user == following:
            raise serializers.ValidationError('Подписка на самого себя запрещена!')
            
        # 2. Проверка на дубликат (вместо UniqueTogetherValidator)
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError('Вы уже подписаны на этого пользователя!')
            
        return data

class GroupSerializer(serializers.ModelSerializer):


    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']
