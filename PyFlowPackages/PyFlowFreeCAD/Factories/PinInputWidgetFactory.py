import weakref
import FreeCAD


from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Widgets.InputWidgets import *

from PyFlow.UI.Widgets.QtSliders import pyf_Slider

from Qt import QtWidgets
from Qt import QtCore
from Qt.QtWidgets import *


FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 5


import numpy as np
from nodeeditor.say import *


class EnumerationInputWidget(InputWidgetSingle):
    """
    String list selection input widget
    """

    def __init__(self, parent=None, **kwds):
        super(EnumerationInputWidget, self).__init__(parent=parent, **kwds)

        self.le = QComboBox(self)
        self.setWidget(self.le)
        self.le.currentIndexChanged.connect(lambda:self.dataSetCallback(self.le.currentText()))


    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        try:
            ix=self.pin._rawPin.values.index(val)
        except:
            ix=0
        self.le.setCurrentIndex(ix)

    def runpin(self):
        '''set data from sel.pin._rawPin'''
        d=self.pin._rawPin._data
        for i,item in enumerate(self.pin._rawPin.values):
            self.le.addItem(item)
        try:
            ix=self.pin._rawPin.values.index(d)
        except:
            ix=0
        self.le.setCurrentIndex(ix)


class Array(object):
    def __init__(self,dat=[]):
        self.dat=np.array(dat)

class VectorInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(VectorInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return FreeCAD.Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(VectorInputWidget, self).resizeEvent(event)


class RotationInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(RotationInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.dsbA = pyf_Slider(self, "float", style=0, name="angle")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)
        self.layout().addWidget(self.dsbA)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
         return FreeCAD.Rotation()
#        return FreeCAD.Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.Axis.x)
        self.dsbY.setValue(val.Axis.y)
        self.dsbZ.setValue(val.Axis.z)


    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(RotationInputWidget, self).resizeEvent(event)


class PlacementInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(PlacementInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        return
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return FreeCAD.Placement()
        #Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        #self.dsbX.setValue(val.x)
        #self.dsbY.setValue(val.y)
        #self.dsbZ.setValue(val.z)
        pass

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(PlacementInputWidget, self).resizeEvent(event)


class ArrayInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(ArrayInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        return
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return Array()
        #Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        #self.dsbX.setValue(val.x)
        #self.dsbY.setValue(val.y)
        #self.dsbZ.setValue(val.z)
        pass

    def XresizeEvent(self, event):
        
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(ArrayInputWidget, self).resizeEvent(event)

    def resizeEvent(self, event):
        super(ArrayInputWidget, self).resizeEvent(event)







class FloatVector3InputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(FloatVector3InputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbX, self.dsbY, self.dsbZ]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Vector3([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(FloatVector3InputWidget, self).resizeEvent(event)




class FloatVector4InputWidget(InputWidgetRaw):
    """Vector4 data input widget"""

    def __init__(self, **kwds):
        super(FloatVector4InputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.dsbW = pyf_Slider(self, "float", style=0, name="w")
        for x in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
            self.layout().addWidget(x)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)
        self.dsbW.valueChanged.connect(self._onDataChangedW)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Vector4([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value(), self.dsbW.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def _onDataChangedW(self, val):
        v = self.asDataTypeClass()
        v.w = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)
        self.dsbW.setValue(val.w)

    def resizeEvent(self, event):
        if self.width() < 340:
            for x in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ, self.dsbW]:
                x.showSlider()
                x.showLabel()
        super(FloatVector4InputWidget, self).resizeEvent(event)


class QuatInputWidget(FloatVector4InputWidget):
    """Quaternion data input widget"""

    def __init__(self, **kwds):
        super(QuatInputWidget, self).__init__(**kwds)

    def asDataTypeClass(self):
        return pyrr.Quaternion([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value(), self.dsbW.value()])


class Matrix33InputWidget(InputWidgetRaw):
    """Matrix33 data input widget"""

    def __init__(self, parent=None, **kwds):
        super(Matrix33InputWidget, self).__init__(parent=parent, **kwds)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbm11 = pyf_Slider(self, "float", style=0)
        self.dsbm12 = pyf_Slider(self, "float", style=0)
        self.dsbm13 = pyf_Slider(self, "float", style=0)
        self.dsbm21 = pyf_Slider(self, "float", style=0)
        self.dsbm22 = pyf_Slider(self, "float", style=0)
        self.dsbm23 = pyf_Slider(self, "float", style=0)
        self.dsbm31 = pyf_Slider(self, "float", style=0)
        self.dsbm32 = pyf_Slider(self, "float", style=0)
        self.dsbm33 = pyf_Slider(self, "float", style=0)

        self.layout().addWidget(self.dsbm22, 1, 1, 1, 1)
        self.layout().addWidget(self.dsbm21, 1, 0, 1, 1)
        self.layout().addWidget(self.dsbm31, 2, 0, 1, 1)
        self.layout().addWidget(self.dsbm23, 1, 2, 1, 1)
        self.layout().addWidget(self.dsbm32, 2, 1, 1, 1)
        self.layout().addWidget(self.dsbm33, 2, 2, 1, 1)
        self.layout().addWidget(self.dsbm12, 0, 1, 1, 1)
        self.layout().addWidget(self.dsbm11, 0, 0, 1, 1)
        self.layout().addWidget(self.dsbm13, 0, 2, 1, 1)
        self._configSpinBoxes()

        self.dsbm11.valueChanged.connect(self.m11Changed)
        self.dsbm12.valueChanged.connect(self.m12Changed)
        self.dsbm13.valueChanged.connect(self.m13Changed)

        self.dsbm21.valueChanged.connect(self.m21Changed)
        self.dsbm22.valueChanged.connect(self.m22Changed)
        self.dsbm23.valueChanged.connect(self.m23Changed)

        self.dsbm31.valueChanged.connect(self.m31Changed)
        self.dsbm32.valueChanged.connect(self.m32Changed)
        self.dsbm33.valueChanged.connect(self.m33Changed)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbm11, self.dsbm12, self.dsbm13,
                  self.dsbm21, self.dsbm22, self.dsbm23,
                  self.dsbm31, self.dsbm32, self.dsbm33]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Matrix33([
            [self.dsbm11.value(), self.dsbm12.value(), self.dsbm13.value()],
            [self.dsbm21.value(), self.dsbm22.value(), self.dsbm23.value()],
            [self.dsbm31.value(), self.dsbm32.value(), self.dsbm33.value()]
        ])

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13,
              self.dsbm21, self.dsbm22, self.dsbm23,
              self.dsbm31, self.dsbm32, self.dsbm33]
        for x in ls:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def m11Changed(self, val):
        m = self.asDataTypeClass()
        m.m11 = val
        self.dataSetCallback(m)

    def m12Changed(self, val):
        m = self.asDataTypeClass()
        m.m12 = val
        self.dataSetCallback(m)

    def m13Changed(self, val):
        m = self.asDataTypeClass()
        m.m13 = val
        self.dataSetCallback(m)

    def m21Changed(self, val):
        m = self.asDataTypeClass()
        m.m21 = val
        self.dataSetCallback(m)

    def m22Changed(self, val):
        m = self.asDataTypeClass()
        m.m22 = val
        self.dataSetCallback(m)

    def m23Changed(self, val):
        m = self.asDataTypeClass()
        m.m23 = val
        self.dataSetCallback(m)

    def m31Changed(self, val):
        m = self.asDataTypeClass()
        m.m31 = val
        self.dataSetCallback(m)

    def m32Changed(self, val):
        m = self.asDataTypeClass()
        m.m32 = val
        self.dataSetCallback(m)

    def m33Changed(self, val):
        m = self.asDataTypeClass()
        m.m33 = val
        self.dataSetCallback(m)

    def setWidgetValue(self, val):
        self.dsbm11.setValue(val.m11)
        self.dsbm12.setValue(val.m12)
        self.dsbm13.setValue(val.m13)

        self.dsbm21.setValue(val.m21)
        self.dsbm22.setValue(val.m22)
        self.dsbm23.setValue(val.m23)

        self.dsbm31.setValue(val.m31)
        self.dsbm32.setValue(val.m32)
        self.dsbm33.setValue(val.m33)

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbm11, self.dsbm12, self.dsbm13,
                      self.dsbm21, self.dsbm22, self.dsbm23,
                      self.dsbm31, self.dsbm32, self.dsbm33]:
                x.hideSlider()
        else:
            for x in [self.dsbm11, self.dsbm12, self.dsbm13,
                      self.dsbm21, self.dsbm22, self.dsbm23,
                      self.dsbm31, self.dsbm32, self.dsbm33]:
                x.showSlider()
        super(Matrix33InputWidget, self).resizeEvent(event)


class Matrix44InputWidget(InputWidgetRaw):
    """Matrix44 data input widget"""

    def __init__(self, parent=None, **kwds):
        super(Matrix44InputWidget, self).__init__(parent=parent, **kwds)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbm11 = pyf_Slider(self, "float", style=0)
        self.dsbm12 = pyf_Slider(self, "float", style=0)
        self.dsbm13 = pyf_Slider(self, "float", style=0)
        self.dsbm14 = pyf_Slider(self, "float", style=0)
        self.dsbm21 = pyf_Slider(self, "float", style=0)
        self.dsbm22 = pyf_Slider(self, "float", style=0)
        self.dsbm23 = pyf_Slider(self, "float", style=0)
        self.dsbm24 = pyf_Slider(self, "float", style=0)
        self.dsbm31 = pyf_Slider(self, "float", style=0)
        self.dsbm32 = pyf_Slider(self, "float", style=0)
        self.dsbm33 = pyf_Slider(self, "float", style=0)
        self.dsbm34 = pyf_Slider(self, "float", style=0)
        self.dsbm41 = pyf_Slider(self, "float", style=0)
        self.dsbm42 = pyf_Slider(self, "float", style=0)
        self.dsbm43 = pyf_Slider(self, "float", style=0)
        self.dsbm44 = pyf_Slider(self, "float", style=0)

        self.layout().addWidget(self.dsbm11, 0, 0, 1, 1)
        self.layout().addWidget(self.dsbm12, 0, 1, 1, 1)
        self.layout().addWidget(self.dsbm13, 0, 2, 1, 1)
        self.layout().addWidget(self.dsbm14, 0, 3, 1, 1)
        self.layout().addWidget(self.dsbm21, 1, 0, 1, 1)
        self.layout().addWidget(self.dsbm22, 1, 1, 1, 1)
        self.layout().addWidget(self.dsbm23, 1, 2, 1, 1)
        self.layout().addWidget(self.dsbm24, 1, 3, 1, 1)
        self.layout().addWidget(self.dsbm31, 2, 0, 1, 1)
        self.layout().addWidget(self.dsbm32, 2, 1, 1, 1)
        self.layout().addWidget(self.dsbm33, 2, 2, 1, 1)
        self.layout().addWidget(self.dsbm34, 2, 3, 1, 1)
        self.layout().addWidget(self.dsbm41, 3, 0, 1, 1)
        self.layout().addWidget(self.dsbm42, 3, 1, 1, 1)
        self.layout().addWidget(self.dsbm43, 3, 2, 1, 1)
        self.layout().addWidget(self.dsbm44, 3, 3, 1, 1)

        self._configSpinBoxes()

        self.dsbm11.valueChanged.connect(self.m11Changed)
        self.dsbm12.valueChanged.connect(self.m12Changed)
        self.dsbm13.valueChanged.connect(self.m13Changed)
        self.dsbm14.valueChanged.connect(self.m14Changed)

        self.dsbm21.valueChanged.connect(self.m21Changed)
        self.dsbm22.valueChanged.connect(self.m22Changed)
        self.dsbm23.valueChanged.connect(self.m23Changed)
        self.dsbm24.valueChanged.connect(self.m24Changed)

        self.dsbm31.valueChanged.connect(self.m31Changed)
        self.dsbm32.valueChanged.connect(self.m32Changed)
        self.dsbm33.valueChanged.connect(self.m33Changed)
        self.dsbm34.valueChanged.connect(self.m34Changed)

        self.dsbm41.valueChanged.connect(self.m41Changed)
        self.dsbm42.valueChanged.connect(self.m42Changed)
        self.dsbm43.valueChanged.connect(self.m43Changed)
        self.dsbm44.valueChanged.connect(self.m44Changed)

    def blockWidgetSignals(self, bLocked):
        for w in [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
                  self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
                  self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
                  self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]:
            w.blockSignals(bLocked)

    def asDataTypeClass(self):
        return pyrr.Matrix44([
            [self.dsbm11.value(), self.dsbm12.value(),
             self.dsbm13.value(), self.dsbm14.value()],
            [self.dsbm21.value(), self.dsbm22.value(),
             self.dsbm23.value(), self.dsbm24.value()],
            [self.dsbm31.value(), self.dsbm32.value(),
             self.dsbm33.value(), self.dsbm34.value()],
            [self.dsbm41.value(), self.dsbm42.value(),
             self.dsbm43.value(), self.dsbm44.value()]
        ])

    def _configSpinBoxes(self):
        ls = [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
              self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
              self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
              self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]
        for x in ls:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def m11Changed(self, val):
        m = self.asDataTypeClass()
        m.m11 = val
        self.dataSetCallback(m)

    def m12Changed(self, val):
        m = self.asDataTypeClass()
        m.m12 = val
        self.dataSetCallback(m)

    def m13Changed(self, val):
        m = self.asDataTypeClass()
        m.m13 = val
        self.dataSetCallback(m)

    def m14Changed(self, val):
        m = self.asDataTypeClass()
        m.m14 = val
        self.dataSetCallback(m)

    def m21Changed(self, val):
        m = self.asDataTypeClass()
        m.m21 = val
        self.dataSetCallback(m)

    def m22Changed(self, val):
        m = self.asDataTypeClass()
        m.m22 = val
        self.dataSetCallback(m)

    def m23Changed(self, val):
        m = self.asDataTypeClass()
        m.m23 = val
        self.dataSetCallback(m)

    def m24Changed(self, val):
        m = self.asDataTypeClass()
        m.m24 = val
        self.dataSetCallback(m)

    def m31Changed(self, val):
        m = self.asDataTypeClass()
        m.m31 = val
        self.dataSetCallback(m)

    def m32Changed(self, val):
        m = self.asDataTypeClass()
        m.m32 = val
        self.dataSetCallback(m)

    def m33Changed(self, val):
        m = self.asDataTypeClass()
        m.m33 = val
        self.dataSetCallback(m)

    def m34Changed(self, val):
        m = self.asDataTypeClass()
        m.m34 = val
        self.dataSetCallback(m)

    def m41Changed(self, val):
        m = self.asDataTypeClass()
        m.m41 = val
        self.dataSetCallback(m)

    def m42Changed(self, val):
        m = self.asDataTypeClass()
        m.m42 = val
        self.dataSetCallback(m)

    def m43Changed(self, val):
        m = self.asDataTypeClass()
        m.m43 = val
        self.dataSetCallback(m)

    def m44Changed(self, val):
        m = self.asDataTypeClass()
        m.m44 = val
        self.dataSetCallback(m)

    def setWidgetValue(self, val):
        self.dsbm11.setValue(val.m11)
        self.dsbm12.setValue(val.m12)
        self.dsbm13.setValue(val.m13)
        self.dsbm14.setValue(val.m14)

        self.dsbm21.setValue(val.m21)
        self.dsbm22.setValue(val.m22)
        self.dsbm23.setValue(val.m23)
        self.dsbm24.setValue(val.m24)

        self.dsbm31.setValue(val.m31)
        self.dsbm32.setValue(val.m32)
        self.dsbm33.setValue(val.m33)
        self.dsbm34.setValue(val.m34)

        self.dsbm41.setValue(val.m41)
        self.dsbm42.setValue(val.m42)
        self.dsbm43.setValue(val.m43)
        self.dsbm44.setValue(val.m44)

    def resizeEvent(self, event):
        if self.width() < 340:
            for x in [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
                      self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
                      self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
                      self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]:
                x.hideSlider()
        else:
            for x in [self.dsbm11, self.dsbm12, self.dsbm13, self.dsbm14,
                      self.dsbm21, self.dsbm22, self.dsbm23, self.dsbm24,
                      self.dsbm31, self.dsbm32, self.dsbm33, self.dsbm34,
                      self.dsbm41, self.dsbm42, self.dsbm43, self.dsbm44]:
                x.showSlider()
        super(Matrix44InputWidget, self).resizeEvent(event)


def getInputWidget(dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT):
    '''
    factory method
    '''
    
    if dataType == 'VectorPin':
        return VectorInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'RotationPin':
        return RotationInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'PlacementPin':
        return PlacementInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'ArrayPin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'FCobjPin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'ShapePin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)

    if dataType == 'EnumerationPin':
        return EnumerationInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)


    if dataType == 'FloatVector3Pin':
        return FloatVector3InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'FloatVector4Pin':
        return FloatVector4InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'QuatPin':
        return QuatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'Matrix33Pin':
        return Matrix33InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    if dataType == 'Matrix44Pin':
        return Matrix44InputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue)
    return None
