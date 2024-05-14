from django_filters import FilterSet
from .models import News

class NewsFilter(FilterSet):
    class Meta:
        model = News
        fields = {
            'title': ['icontains'],
            'content': ['icontains'],
            'author': ['icontains'],
            'created_at': ['icontains'],
        }