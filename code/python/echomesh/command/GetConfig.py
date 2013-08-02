from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Join
from echomesh.command import CommandRegistry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

GET_ARGUMENT_ERROR = """
"get" needs one or more arguments.

Example:
  get audio.input.enable
"""

def _route_items(items, successes, failures):
  for v in items:
    try:
      successes.append([v, Config.get(*v.split('.'))])
    except:
      failures.append(v)


def get_config(_, *items):
  if not items:
    items =
  failures = []
  successes = []
  for v in items:
    try:
      successes.append([v, Config.get(*v.split('.'))])
    except:
      failures.append(v)

  for value, result in successes:
    LOGGER.info('%s=%s', value, result)
  if failures:
    LOGGER.error('Didn\'t understand %s', Join.join_words(failures))

GET_HELP = """
  Prints one or more configuration variables.

Examples:
  config.get speed
  config.get audio.input.enabled audio.output.enabled
"""

CommandRegistry.register(get_config, 'get', GET_HELP)
