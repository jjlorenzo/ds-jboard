import argparse
import os

import poetry_version

__version__ = poetry_version.extract(__file__)


def entry_point():
  parser = argparse.ArgumentParser()
  parser.add_argument("--version", action="version", version=__version__)
  parser.add_argument("--prod", default=False, action="store_true")
  parser.add_argument("cmd")
  parser.add_argument("argv", nargs="*")
  args = parser.parse_args()

  os.environ["DJANGO_DEBUG"] = str(not args.prod)

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
        UWSGI_WSGI="jboard.wsgi:application",
      )
      os.execvp("uwsgi", ("uwsgi", "--http=0.0.0.0:8000"))
    else:
      os.execvp("poetry", ("poetry", "run", "django-admin", "runserver", "0.0.0.0:8000"))
  raise NotImplementedError(args.cmd)
