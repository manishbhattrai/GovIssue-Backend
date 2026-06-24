from rest_framework import serializers
from broadcasts.models import Broadcast, BroadcastComment, BroadcastVote
from django.db.models import Sum

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.full_name')
    user_image = serializers.ImageField(source='user.profile_image', read_only=True)
    is_admin = serializers.ReadOnlyField(source='user.is_admin')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = BroadcastComment
        fields = ['id', 'user_name', 'text', 'parent',
                  'created_at', 'replies','user_image','is_admin',]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class BroadcastSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_name = serializers.ReadOnlyField(source='created_by.full_name')
    vote_score = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    up_count = serializers.SerializerMethodField()
    down_count = serializers.SerializerMethodField()

    class Meta:
        model = Broadcast
        fields = [
            'id', 'title', 'message', 'category', 'category_name',
            'author_name', 'created_at', 'is_active',
            'comments_enabled', 'vote_score', 'user_vote', 'comments','up_count',
            'down_count',
        ]

    def get_vote_score(self, obj):
        return obj.votes.aggregate(Sum('vote_type'))['vote_type__sum'] or 0

    def get_comments(self, obj):
        if not obj.comments_enabled:
            return []
        queryset = obj.comments.filter(parent=None)
        return CommentSerializer(queryset, many=True).data

    def get_up_count(self, obj):
        return obj.votes.filter(vote_type=1).count()

    def get_down_count(self, obj):
        # This returns the count of records, which is naturally positive (e.g., 5 downvotes)
        return obj.votes.filter(vote_type=-1).count()

    def get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            vote = obj.votes.filter(user=user).first()
            if vote:
                return 'up' if vote.vote_type == 1 else 'down'
        return None

class CommentCreateSerializer(serializers.Serializer):
    parent = serializers.IntegerField(required=False, allow_null=True)
    text = serializers.CharField()

class VoteCreateSerializer(serializers.Serializer):
    type  = serializers.ChoiceField(choices=['up','down'])
