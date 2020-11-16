import datetime

from playhouse.postgres_ext import *

database = PostgresqlExtDatabase("db-8200", host="postgres", user="postgres")


def create_tables():
  with database:
    database.create_tables([Search])


class Search(Model):
  description = CharField(max_length=20)
  location    = CharField(max_length=20)
  search_at   = DateTimeTZField(default=datetime.datetime.utcnow)
  search_from = IPField()

  class Meta:
    database = database
    table_name = "jboard_search"
