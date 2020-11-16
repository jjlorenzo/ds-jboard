import flask

from ..consumers import GithubJobsConsumer
from ..models import Search
from ..models import database

consumer = GithubJobsConsumer(base_url="https://jobs.github.com/")


search_response_keys = {
  "id",
  "type",
  "created_at",
  "company",
  "location",
  "title",
}


def search(**kwargs):
  search_from = flask.request.headers.get("X-Real-Ip", flask.request.remote_addr)
  with database:
    response_data = consumer.positions(**kwargs)
    Search.create(**kwargs, search_from=search_from)
    return [{
      key: val
      for key, val in item.items()
      if key in search_response_keys
    } for item in response_data]


get_response_keys = {
  "id",
  "type",
  "created_at",
  "company",
  "company_url",
  "location",
  "title",
  "description",
  "how_to_apply",
  "company_logo",
}


def get(**kwargs):
  return {
    key: val
    for key, val in consumer.position(**kwargs).items()
    if key in get_response_keys
  }
