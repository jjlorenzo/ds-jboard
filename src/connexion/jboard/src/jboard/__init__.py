import argparse
import os
import sys

import connexion
import poetry_version

from .models import create_tables

__version__ = poetry_version.extract(__file__)


def create_app():
  connexion_app = connexion.App(__name__, specification_dir="specs/")
  connexion_api = connexion_app.add_api(
    resolver=connexion.RestyResolver("jboard.viewsets"),
    specification="v1.yaml",
    strict_validation=True,
    validate_responses=True,
  )
  flask_app = connexion_app.app
  flask_app.config["JSON_SORT_KEYS"] = False
  flask_app.config["spec"] = connexion_api.specification
  return flask_app


def entry_point():
  parser = argparse.ArgumentParser()
  parser.add_argument("--version", action="version", version=__version__)
  parser.add_argument("--prod", default=False, action="store_true")
  parser.add_argument("cmd")
  parser.add_argument("argv", nargs="*")
  args = parser.parse_args()

  os.environ["FLASK_ENV"] = "production" if args.prod else "development"

  if args.cmd == "create-tables":
    create_tables()
    sys.exit()

  if args.cmd == "server":
    if args.prod:
      os.environ.update(
        UWSGI_AUTO_PROCNAME="1",
        UWSGI_ENABLE_THREADS="1",
        UWSGI_MASTER="1",
        UWSGI_PLUGIN="python,http",
        UWSGI_SHOW_CONFIG="1",
        UWSGI_SINGLE_INTERPRETER="1",
        UWSGI_THUNDER_LOCK="1",
        UWSGI_UID="nobody",
        UWSGI_VENV=".venv",
        UWSGI_WSGI="jboard:create_app()",
      )
      os.execvp("uwsgi", ("uwsgi", "--http=0.0.0.0:8000"))
    else:
      os.execvp("poetry", ("poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8000"))
  raise NotImplementedError(args.cmd)
