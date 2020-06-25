from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from posts.models import Post, Follow, User

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        followers = User.objects.filter(follower__author=user)
        email_pool = [user.email for user in followers]
        send_mail(
            'New post!', f'{user.first_name} {user.last_name} posted something, check it out!', 'notifier@yatube.com', email_pool, fail_silently=False
        )