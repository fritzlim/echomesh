from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Audio(Element.Element):
  def __init__(self, parent, description):
    super(Audio, self).__init__(parent, description)
    if Config.get('audio', 'output', 'enable'):
      from echomesh.sound import FilePlayer
      self.add_mutual_stop_slave(FilePlayer.play(**description))
    else:
      LOGGER.debug('Audio disabled for %s', description.get('file', None))

# TODO: config client.

Element.register(Audio)