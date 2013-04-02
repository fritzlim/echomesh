from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.base import Config
from echomesh.color import LightsEnabled
from echomesh.color.LightBank import LightBank
from echomesh.util import Log

_LATCH_BYTE_COUNT = 3
_LATCH = bytearray(0 for i in xrange(LATCH_BYTE_COUNT))

_INTERNAL_LATCH_BYTE_COUNT = 0

class SPILightBank(LightBank):
  RGB = lambda r, g, b: (r, g, b)
  GRB = lambda r, g, b: (g, r, b)
  BRG = lambda r, g, b: (b, r, g)

  def __init__(self, count=None):
    assert LightsEnabled.lights_enabled(), "Lighting is not enabled."

    super(SPILightBank, self).__init__(count=count)
    order = Config.get('light', 'order')
    self.order = getattr(LightBank, order.upper(), None)
    if not self.order:
      LOGGER.error("Didn't understand order %s", order)
    self._clear, self._bank = self._light_array(), self._light_array()

  def _light_array(self):
    b = bytearray(x for i in xrange(self.count + _INTERNAL_LATCH_BYTE_COUNT))
    for i in xrange(_INTERNAL_LATCH_BYTE_COUNT):
      b[-1 - i] = 0
    return b

  def _write(self, lights):
    self._device.write(lights)
    self._device.flush()
    if _LATCH_BYTE_COUNT:
      self._device.write(_LATCH)
      self._device.flush()

  def clear(self):
    with self.lock:
      self._write(self._clear)

  def _before_thread_start(self):
    super(SPILightBank, self)._before_thread_start()
    self._device = open('/dev/spidev0.0', 'wb')

  def _after_thread_pause(self):
    super(SPILightBank, self)._after_thread_pause()
    self._device.close()
    self._device = None

  def _display_lights(self, lights):
    for i, light in enumerate(lights):
      if light is None:
        light = [0x80, 0x80, 0x80]
      else:
        light =  self.order(*int(0x80 + 0x7F * x) for x in light)
      self._bank[3 * i:3 * (i + 1)] = light
    self._write(self.pattern)