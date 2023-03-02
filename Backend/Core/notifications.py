from notifications.models import Notification


def get_unread_notifications(user):
    unread_notifications = Notification.objects.unread().filter(recipient=user)
    return unread_notifications


def count_notifications_unreade(user):
    return get_unread_notifications(user).count()