from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from compatibility.weakref import WeakSet

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import MergeConfig
from echomesh.base import Name

CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = WeakSet()

THROW_EXCEPTIONS = True

def reconfigure():
  _fix_home_directory_environment_variable()

  global CONFIG, CONFIGS_UNVISITED
  CONFIG = MergeConfig.reconfigure()
  CONFIGS_UNVISITED = copy.deepcopy(CONFIG)

  _get_name_and_tags()

def add_client(client):
  if not client in CLIENTS:
    CLIENTS.add(client)
    client.config_update(get)

def update_clients():
  for c in CLIENTS:
    try:
      c.config_update(get)
    except:
      if THROW_EXCEPTIONS:
        raise

def get(*parts):
  config, unvisited = CONFIG, CONFIGS_UNVISITED
  none = object()
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s: %s" %
                      ('.'.join(parts), config))
    value = config.get(part, none)
    if value is none:
      raise Exception('Couldn\'t find configuration "%s"' % '.'.join(parts))
    return value

  for part in parts[:-1]:
    config = get_part(config, part)
    if unvisited:
      unvisited = unvisited.get(part)

  last_part = parts[-1]
  value = get_part(config, last_part)

  try:
    del unvisited[last_part]
  except:
    pass

  return value

def assign(values):
  return MergeConfig.merge_assignments(CONFIG, Args.split(values))

def assign_and_update(values):
  assignments = assign(values)
  if assignments:
    update_clients()
  return assignments

def get_unvisited():
  def fix(d):
    if isinstance(d, dict):
      for k, v in list(d.iteritems()):
        assert v is not None
        fix(v)
        if v == {}:
          del d[k]
    return d
  if not True:
    return CONFIGS_UNVISITED
  return fix(copy.deepcopy(CONFIGS_UNVISITED))


_HOME_VARIABLE_FIXED = False;

def _fix_home_directory_environment_variable():
  if not _HOME_VARIABLE_FIXED:
    # If running as root, export user pi's home directory as $HOME.
    if getpass.getuser() == 'root':
      os.environ['HOME'] = '/home/pi'
    _HOME_VARIABLE_FIXED = True

def _get_name_and_tags():
  name = Name.lookup(get('map', 'name'))
  if name:
    Name.set_name(name)

  tags = Name.lookup(get('map', 'tag'))
  if tags:
    if isinstance(tags, six.string_types):
      tags = [tags]
    Name.TAGS = tags

  if name or tags:
    CommandFile.compute_command_path()
