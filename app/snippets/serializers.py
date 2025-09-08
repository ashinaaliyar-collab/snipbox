from rest_framework import serializers
from django.urls import reverse

from snippets.models import Snippet, Tag

class SnippetSerializer(serializers.ModelSerializer):
    tag = serializers.CharField()
    created_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Snippet
        fields = ('title', 'note', 'tag', 'created_on', 'updated_on')

    def create(self, validated_data):
        tag_title = validated_data.pop('tag')
        tag, created = Tag.objects.get_or_create(title=tag_title, defaults={'updated_by': self.context['request'].user.user_obj})
        validated_data['tag'] = tag
        validated_data['updated_by'] = self.context['request'].user.user_obj
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'tag' in validated_data:
            tag_title = validated_data.pop('tag')
            tag, created = Tag.objects.get_or_create(title=tag_title, defaults={'updated_by': self.context['request'].user.user_obj})
            validated_data['tag'] = tag
        validated_data['updated_by'] = self.context['request'].user.user_obj
        return super().update(instance, validated_data)
    

class TagSerializer(serializers.ModelSerializer):

    def validate_title(self, value):
        if Tag.objects.filter(title=value).exists():
            raise serializers.ValidationError("Tag title must be unique.")
        return value
    
    class Meta:
        model = Tag
        fields = ('id', 'title')


class SnippetOverviewSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    created_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def get_detail_url(self, obj):
        request = self.context.get('request')
        url = reverse('SnippetDetailView', args=[obj.id])
        return request.build_absolute_uri(url) if request else url

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'note', 'created_on', 'updated_on', 'detail_url')

    