
import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

  initial = True

  dependencies = [
  ]

  operations = [
    migrations.CreateModel(
      name="Search",
      fields=[
        ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("description", models.CharField(max_length=20)),
        ("location", models.CharField(max_length=20)),
        ("search_at", models.DateTimeField(default=django.utils.timezone.now)),
        ("search_from", models.GenericIPAddressField()),
      ],
    ),
  ]
