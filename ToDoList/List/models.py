from django.db import models
from django.db.models import Model


class Post(models.Model):
    title = models.CharField('Название', max_length=250)
    url = models.URLField('Адрес')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    text = models.TextField()
    from_post = models.ForeignKey(Post, on_delete=models.CASCADE)
