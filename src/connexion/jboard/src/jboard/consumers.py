from connexion import ProblemException
from uplink import Consumer
from uplink import Path
from uplink import Query
from uplink import get
from uplink import response_handler
from uplink import returns


def handle_response(res):
  if 200 <= res.status_code < 300:
    return res
  raise ProblemException(status=res.status_code, title=res.reason, instance=res.url)


class GithubJobsConsumer(Consumer):

  @returns.json
  @response_handler(handle_response)
  @get("positions.json")
  def positions(self, description: Query = None, location: Query = None, page: Query = 1):
    pass

  @returns.json
  @response_handler(handle_response)
  @get("positions/{id}.json")
  def position(self, id: Path, md: Query("markdown") = None):
    pass
