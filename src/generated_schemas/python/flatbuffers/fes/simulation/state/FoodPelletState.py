# automatically generated by the FlatBuffers compiler, do not modify

# namespace: state

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class FoodPelletState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FoodPelletState()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFoodPelletState(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # FoodPelletState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FoodPelletState
    def Id(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # FoodPelletState
    def Pos(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from fes.simulation.state.Vec2f import Vec2f
            obj = Vec2f()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def FoodPelletStateStart(builder):
    builder.StartObject(2)

def Start(builder):
    FoodPelletStateStart(builder)

def FoodPelletStateAddId(builder, id):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(id), 0)

def AddId(builder, id):
    FoodPelletStateAddId(builder, id)

def FoodPelletStateAddPos(builder, pos):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(pos), 0)

def AddPos(builder, pos):
    FoodPelletStateAddPos(builder, pos)

def FoodPelletStateEnd(builder):
    return builder.EndObject()

def End(builder):
    return FoodPelletStateEnd(builder)
