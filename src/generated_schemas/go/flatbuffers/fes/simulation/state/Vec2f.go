// Code generated by the FlatBuffers compiler. DO NOT EDIT.

package state

import (
	flatbuffers "github.com/google/flatbuffers/go"
)

type Vec2f struct {
	_tab flatbuffers.Struct
}

func (rcv *Vec2f) Init(buf []byte, i flatbuffers.UOffsetT) {
	rcv._tab.Bytes = buf
	rcv._tab.Pos = i
}

func (rcv *Vec2f) Table() flatbuffers.Table {
	return rcv._tab.Table
}

func (rcv *Vec2f) X() float32 {
	return rcv._tab.GetFloat32(rcv._tab.Pos + flatbuffers.UOffsetT(0))
}
func (rcv *Vec2f) MutateX(n float32) bool {
	return rcv._tab.MutateFloat32(rcv._tab.Pos+flatbuffers.UOffsetT(0), n)
}

func (rcv *Vec2f) Y() float32 {
	return rcv._tab.GetFloat32(rcv._tab.Pos + flatbuffers.UOffsetT(4))
}
func (rcv *Vec2f) MutateY(n float32) bool {
	return rcv._tab.MutateFloat32(rcv._tab.Pos+flatbuffers.UOffsetT(4), n)
}

func CreateVec2f(builder *flatbuffers.Builder, x float32, y float32) flatbuffers.UOffsetT {
	builder.Prep(4, 8)
	builder.PrependFloat32(y)
	builder.PrependFloat32(x)
	return builder.Offset()
}
