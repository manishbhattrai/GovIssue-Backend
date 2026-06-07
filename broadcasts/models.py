from django.db import models
from django.conf import settings

class Broadcast(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='broadcasts/', null=True, blank=True)
    message = models.TextField()
    category = models.ForeignKey('issues.Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    comments_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class BroadcastVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    broadcast = models.ForeignKey(Broadcast, related_name='votes', on_delete=models.CASCADE)
    # 1 for Upvote, -1 for Downvote
    vote_type = models.IntegerField()

    class Meta:
        unique_together = ('user', 'broadcast')

class BroadcastComment(models.Model):
    broadcast = models.ForeignKey(Broadcast, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    # Self-referential for nesting
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']