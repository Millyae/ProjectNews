from celery import shared_task
from django.core.mail import send_mail
from .models import *

@shared_task()
def send_notification(news_id):
    news = News.objects.get(id=news_id)
    subscribers = news.subscribers.all()
    recipients = [subscribers.email for subscriber in subscribers]
    subject = "Уведомление о новой новости"
    message = f"Появилась новая новость: {news.title}. Прочитать:{news.get_absolute_url()}"
    send_mail(subject, message, 'your_email@example.com', recipients)

@shared_task()
def send_weekly_newsletter():
    latest_news = News.objects.order_by('-created_at')[:5]
    recipients = []
    for news in latest_news:
        recipients += [subscriber.email for subscriber in news.subscribers.all()]
    recipients = list(set(recipients))
    subject = "Еженедельная рассылка новостей"
    message = "Последние новости:\n"
    for news in latest_news:
        message += f"- {news.title}: {news.get_absolute_url()}\n"
    send_mail(subject, message, 'your_email@example.com', recipients)