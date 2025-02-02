from .models import Notification
from django.db.models import Q

def notification_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user),
            is_read=False
        ).count()
    else:
        unread_count = 0
    return {'unread_notifications_count': unread_count}
