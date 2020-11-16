from django.db import models
from django.utils import timezone


class SearchManager(models.Manager):
  def create(self, **kwargs):
    kwargs.pop("page")
    super().create(**kwargs)


class Search(models.Model):
  description = models.CharField(max_length=20)
  location    = models.CharField(max_length=20)
  search_at   = models.DateTimeField(default=timezone.now)
  search_from = models.GenericIPAddressField()

  objects = SearchManager()
