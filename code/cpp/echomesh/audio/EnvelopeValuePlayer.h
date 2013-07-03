#ifndef __ECHOMESH_ENVELOPEVALUEPLAYER__
#define __ECHOMESH_ENVELOPEVALUEPLAYER__

#include "echomesh/audio/Envelope.h"

namespace echomesh {

class EnvelopeValuePlayer {
 public:
  typedef std::pair<Envelope::Point, Envelope::Point> Segment;
  typedef vector<Segment> SegmentList;

  EnvelopeValuePlayer(const EnvelopeValue&);
  bool isConstant() const { return envelopeValue_.isConstant; }

  const Envelope::Point point() const { return point_; }
  const Envelope::PointList& points() const {
    return envelopeValue_.envelope.points;
  }

  void begin();

  // Only call this if isConstant is false.
  SegmentList getSegments(SampleTime);

 private:
  const EnvelopeValue& envelopeValue_;
  const bool isConstant_;

  Envelope::Point point_;
  int index_;
  int loops_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EnvelopeValuePlayer);
};

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPEVALUEPLAYER__