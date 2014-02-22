cdef extern from "echomesh/component/InstrumentGrid.h" namespace "echomesh":
  cdef cppclass InstrumentGrid:
    InstrumentGrid()

    void setLights(FColorList)
    void setPaintingIsUnclipped(bool)
    void setLightCount(int)
    void setLabelStartsAtZero(bool)
    void setLayout(
      Point layout, Point size, Point padding,
      Point instrumentPadding, Point labelPadding)
    void setShowLabel(bool)
    int getLightCount()

