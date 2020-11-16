from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view
from rest_framework.schemas import openapi

from .viewsets import PositionsViewSet
from .schema import SchemaGenerator

apiv1 = routers.SimpleRouter(trailing_slash=False)
apiv1.register("positions", PositionsViewSet, basename="position")


apiv1_schema_view = get_schema_view(
  description="DjangoRestFramework framework",
  generator_class=SchemaGenerator,
  patterns=apiv1.urls,
  public=True,
  renderer_classes=[JSONOpenAPIRenderer],
  title="Jobs Board Backend",
  url="/api/v1",
  version="1",
)

urlpatterns = [
  path("api/v1/", include((apiv1.urls, "api"), namespace="api-v1")),
  path("api/v1/openapi.json", apiv1_schema_view, name="api-v1-schema")
]
