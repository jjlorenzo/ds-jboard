from django.urls import reverse
from rest_framework import serializers

DESCRIPTION_CHOICES = [
  "Go",
  "Java",
  "Javascript",
  "Python",
  "React",
  "Ruby",
]

LOCATION_CHOICES = [
  "Beijing",
  "Chicago",
  "London",
  "Paris",
  "Phoenix",
  "San Francisco",
]


class PositionListSerializer:

  class Request(serializers.Serializer):
    description = serializers.ChoiceField(choices=DESCRIPTION_CHOICES)
    location    = serializers.ChoiceField(choices=LOCATION_CHOICES)
    page        = serializers.IntegerField(default=1, min_value=1)
    search_from = serializers.IPAddressField(write_only=True)

  class Response(serializers.Serializer):
    id         = serializers.CharField()
    type       = serializers.CharField()
    created_at = serializers.CharField()
    company    = serializers.CharField()
    location   = serializers.CharField()
    title      = serializers.CharField()


class PositionRetrieveSerializer:

  class Request(serializers.Serializer):
    id = serializers.CharField()
    md = serializers.ChoiceField(choices=["true", "false"], required=False)

  class Response(serializers.Serializer):
    id           = serializers.CharField()
    type         = serializers.CharField()
    created_at   = serializers.CharField()
    company      = serializers.CharField()
    company_url  = serializers.CharField()
    location     = serializers.CharField()
    title        = serializers.CharField()
    description  = serializers.CharField(trim_whitespace=False)
    how_to_apply = serializers.CharField(trim_whitespace=False)
    company_logo = serializers.CharField(allow_null=True)
