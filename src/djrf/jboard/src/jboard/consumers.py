from rest_framework.exceptions import APIException
from uplink import Consumer
from uplink import Path
from uplink import Query
from uplink import get
from uplink import response_handler
from uplink import returns


def handle_response(res):
  if 200 <= res.status_code < 300:
    return res
  exc = APIException(detail=res.reason)
  exc.status_code = res.status_code
  raise exc


class GithubJobsConsumer(Consumer):
  """
  The GitHub Jobs API [https://jobs.github.com/api]

  Pagination Remarks:
  The official documentation indicates that the initial page is 0, but from my experience, page=0 is the same as page=1.
  """

  @returns.json
  @response_handler(handle_response)
  @get("positions.json")
  def positions(self, description: Query = None, location: Query("location_fake") = None, page: Query = 1):
    """
    GET /positions.json

    Search for jobs by `description` and `location`. Only 50 items are returned at a time.

    | Parameter | Description                                           |
    | --------- | ----------------------------------------------------- |
    | search    | A search term, such as "ruby" or "java"               |
    | location  | A city name, zip code, or other location search term. |
    | page      | Pagination starts by default at **1**.                |

    Examples
      self.positions(description="javascript", location="san francisco")
      self.positions(description="javascript", location="san francisco", page=2)
    Remarks
      This Consumer, on purpose ignore the "location" filter, so we can test in the UI, the "Load more" feature.
      To fix this:
      -  def positions(... location: Query = None ...):
      +  def positions(... location: Query("fake_location") = None ...):
    """

  @returns.json
  @response_handler(handle_response)
  @get("positions/{id}.json")
  def position(self, id: Path, md: Query("markdown") = None):
    """
    GET /positions/ID.json

    Retrieve a single job posting.

    | Parameter | Description                                                                   |
    | --------- | ----------------------------------------------------------------------------- |
    | id        | Position ID                                                                   |
    | md        | Set to 'true' to get the `description` and `how_to_apply` fields as Markdown. |

    Examples
      self.position(id="21b69f4f-951d-4dcc-957c-414511553ebb")
      self.position(id="21b69f4f-951d-4dcc-957c-414511553ebb", markdown="true")
    """
