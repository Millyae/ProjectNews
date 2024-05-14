from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta

class News(models.Model):
    title = models.CharField(max_length=255, unique=True, default='')
    content = models.TextField(default='')
    author = models.CharField(max_length=40, unique=False, default='')
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to', blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def clean(self):
        today = datetime.now(). date()
        user_news_count = News.objects.filter(author = self.author, created_at__gte=today).count()
        if user_news_count>=3:
            raise ValueError("Пользователь не может опубликовать более трех новостей в сутки")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def notify_subscribers(self):
        subscribers = self.subscribers.all()
        subject = f"Новая статья в категории {self.category}"
        for subscriber in subscribers:
            message = render_to_string('email/notification.html', {'news': self, 'subscriber': subscriber})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'your_email@example.com', [subscriber.email], html_message=message)

@receiver(post_save, sender=News)
def check_daily_news_limit(sender, instance, **kwargs):
    user = instance.author
    news_count = News.objects.filter(author=user, created_at__gte=timezone.now() - timedelta(days=1)).count()
    if news_count > 3:
        instance.delete()

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name