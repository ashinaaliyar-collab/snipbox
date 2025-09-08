from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from snippets.models import Snippet, Tag
from snippets.serializers import SnippetSerializer, TagSerializer, SnippetOverviewSerializer
from usermanagement.mixins import StandardResponseMixin

class SnippetCreateView(StandardResponseMixin, generics.CreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = [permissions.IsAuthenticated]

class SnippetDetailView(StandardResponseMixin, generics.RetrieveAPIView):
    serializer_class = SnippetSerializer

    def get_queryset(self):
        user = self.request.user
        return Snippet.objects.filter(is_active=True, updated_by__user=user)

class SnippetUpdateView(StandardResponseMixin, generics.UpdateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Snippet.objects.filter(is_active=True, updated_by__user=user)

class SnippetDeleteView(StandardResponseMixin, generics.DestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Snippet.objects.filter(is_active=True, updated_by__user=user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        snippets = self.get_queryset()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class TagListView(StandardResponseMixin, generics.ListAPIView):
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagDetailView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        user = self.request.user
        return Snippet.objects.filter(tag_id=tag_id, is_active=True, updated_by__user=user)

class SnippetOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        snippets = Snippet.objects.filter(updated_by__user=user)
        total_count = snippets.count()
        snippet_list = SnippetOverviewSerializer(snippets, many=True).data
        return Response({
            'message': "Listed successfully",
            'total_count': total_count,
            'snippets': snippet_list
        })

