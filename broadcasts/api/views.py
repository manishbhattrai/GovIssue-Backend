from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from broadcasts.models import Broadcast, BroadcastVote, BroadcastComment
from .serializers import BroadcastSerializer, CommentSerializer, CommentCreateSerializer, VoteCreateSerializer


class BroadcastViewSet(viewsets.ModelViewSet):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Broadcast.objects.all()
        return Broadcast.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'vote', 'comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        broadcast = self.get_object()

        serializer = VoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #v_type = request.data.get('type')

        v_type = serializer.validated_data['type']
        score = 1 if v_type == 'up' else -1

        vote, created = BroadcastVote.objects.get_or_create(
            user=request.user,
            broadcast=broadcast,
            defaults={'vote_type': score}
        )

        if not created:
            if vote.vote_type == score:
                vote.delete()
            else:
                vote.vote_type = score
                vote.save()

        return Response({'status': 'vote processed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        broadcast = self.get_object()
        if not broadcast.comments_enabled:
            return Response({'error': 'Comments are disabled'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #parent_id = request.data.get('parent')
        #text = request.data.get('text')

        parent_id = serializer.validated_data.get('parent')
        text = serializer.validated_data['text']

        if parent_id:
            if not BroadcastComment.objects.filter(id=parent_id,broadcast=broadcast).exists():
                return Response({"error":"Invalid parent comment"}, status=status.HTTP_400_BAD_REQUEST)

        comment = BroadcastComment.objects.create(
            broadcast=broadcast,
            user=request.user,
            text=text,
            parent_id=parent_id
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)