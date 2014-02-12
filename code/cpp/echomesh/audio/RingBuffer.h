#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class RingBuffer {
 public:
  RingBuffer(int channels, int size);
  void append(int count, const float** samples);
  void remove(AudioSampleBuffer* buffer);

 private:
  AudioSampleBuffer buffer_;
  int begin_, end_, overruns_, underruns_;
  const int channels_;
  const int size_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(RingBuffer);
};

}  // namespace audio
}  // namespace echomesh