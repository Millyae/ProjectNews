from django import forms
from .models import News

class NewsForms(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'content',
            'author',
            'created_at',
        ]
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'})
        }

        def clean(self):
            cleaned_data = super().clean()
            content = cleaned_data.get("content")
            title = cleaned_data.get("title")
            if content and len(content) < 20:
                self.add_error('content', 'Содержание не может быть меньше 20 символов')

            if title and len(title) < 5:
                self.add_error('title', 'Заголовок должен содержать не менее 5 символов')

            return cleaned_data
