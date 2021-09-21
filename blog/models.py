from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(verbose_name='Titulo', max_length=200, blank=True)
    text = models.TextField(verbose_name='Texto', null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('published_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
class Pictures(models.Model):
    pass
    # post = models.ForeignKey(Post)
    # img = models.
