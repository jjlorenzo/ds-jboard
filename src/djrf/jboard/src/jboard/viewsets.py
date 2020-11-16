from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .consumers import GithubJobsConsumer
from .models import Search
from .serializers import PositionListSerializer
from .serializers import PositionRetrieveSerializer


class PositionsViewSet(viewsets.ViewSet):

  def get_serializer_class(self, for_request=True):
    if self.action == "list":
      return getattr(PositionListSerializer, "Request" if for_request else "Response")
    if self.action == "retrieve":
      return getattr(PositionRetrieveSerializer, "Request" if for_request else "Response")
    raise AssertionError(f"get_serializer_class: not handle action '${self.action}'")

  consumer = GithubJobsConsumer(base_url=settings.GITHUB_JOBS_CONSUMER_BASE_URL)

  def list(self, request):
    search_from = request.META.get("HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR"))
    request_data = request.query_params.copy()
    request_data.update(search_from=search_from)
    serializer = PositionListSerializer.Request(data=request_data)
    if serializer.is_valid():
      response_data = self.consumer.positions(**serializer.data)
      response = PositionListSerializer.Response(data=response_data, many=True)
      if response.is_valid():
        Search.objects.create(**serializer.validated_data)
        return Response(response.data)
      return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, pk=None):
    request_data = request.query_params.copy()
    request_data.update(id=pk)
    serializer = PositionRetrieveSerializer.Request(data=request_data)
    if serializer.is_valid():
      response = PositionRetrieveSerializer.Response(data=self.consumer.position(**serializer.data))
      if response.is_valid():
        return Response(response.data)
      return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
