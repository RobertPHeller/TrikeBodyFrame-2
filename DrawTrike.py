#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed Apr 10 07:45:28 2024
#  Last Modified : <240411.1716>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
#*****************************************************************************


import Part
from FreeCAD import Base
import FreeCAD as App
import os
import sys
sys.path.append(os.path.dirname(__file__))
import Mesh

import datetime

from abc import ABCMeta, abstractmethod, abstractproperty

def IntToString(i):
    return "%d" % i

class TerraTrike(object):
    _crankCenter = Base.Vector(-431.800,0,355.600)
    _boomBottom  = Base.Vector(0,0,165.100)
    _belowSeatBack = Base.Vector(711.200,0,228.923)
    _rightRearForkA = Base.Vector(711.200,-((5.75/2)*25.4),228.923)
    _rightRearForkB = Base.Vector(990.6,-((5.75/2)*25.4),254.000)
    _leftRearForkA = Base.Vector(711.200,((5.75/2)*25.4),228.923)
    _leftRearForkB = Base.Vector(990.6,((5.75/2)*25.4),254.000)
    _rearWheelAxle = Base.Vector(990.6,0,254.000)
    _rightFrontAxle = Base.Vector(0,-330.200,254.000)
    _leftFrontAxle = Base.Vector(0,330.200,254.000)
    _crankRadius = 203.200
    _crankSpace = 6*25.4
    _wheelRadius = 254.000
    _wheelThick = 35
    _frameTubeDiameter = 1.75*25.4
    _rearForkTubeDiameter = 1.0*25.4
    _rearForkWidth = 5.75*25.4
    _rearForkSpread = 5*25.4
    _rearForkSpreadTubeDiameter = .75*25.4
    def _wheel(self,center):
        norm = Base.Vector(0,1,0)
        extrude = Base.Vector(0,self._wheelThick,0)
        return Part.Face(Part.Wire(\
            Part.makeCircle(self._wheelRadius,\
                            center.add(Base.Vector(0,-(self._wheelThick/2),0)),\
                            norm))).extrude(extrude)
    def _frameTube(self,r,a,b):
        extrude = b.sub(a)
        return Part.Face(Part.Wire(\
                Part.makeCircle(r,self.origin.add(a),extrude)))\
                    .extrude(extrude)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.rearWheel = self._wheel(origin.add(self._rearWheelAxle))
        self.rightFrontWheel = self._wheel(origin.add(self._rightFrontAxle))
        self.leftFrontWheel = self._wheel(origin.add(self._leftFrontAxle))
        frame = self._frameTube(self._frameTubeDiameter/2.0,\
                                self._boomBottom,\
                                self._crankCenter)
        frame = frame.fuse(self._frameTube(self._frameTubeDiameter/2.0,\
                                           self._boomBottom,\
                                           self._rightFrontAxle))
        frame = frame.fuse(self._frameTube(self._frameTubeDiameter/2.0,\
                                           self._boomBottom,\
                                           self._leftFrontAxle))
        frame = frame.fuse(self._frameTube(self._frameTubeDiameter/2.0,\
                                           self._boomBottom,\
                                           self._belowSeatBack))
        frame = frame.fuse(self._frameTube(self._rearForkSpreadTubeDiameter/2.0,\
                                           self._rightRearForkA,\
                                           self._leftRearForkA))
        frame = frame.fuse(self._frameTube(self._rearForkTubeDiameter/2.0,\
                                           self._rightRearForkA,\
                                           self._rightRearForkB))
        frame = frame.fuse(self._frameTube(self._rearForkTubeDiameter/2.0,\
                                           self._leftRearForkA,\
                                           self._leftRearForkB))
        self.frame = frame
        crankExtrude = Base.Vector(0,2*self._crankSpace,0)
        crankNorm = Base.Vector(0,1,0)
        crankOrigin = origin.add(self._crankCenter).sub(Base.Vector(0,self._crankSpace,0))
        self.crank = Part.Face(Part.Wire(\
                        Part.makeCircle(self._crankRadius,\
                                        crankOrigin,\
                                        crankNorm)))\
                            .extrude(crankExtrude)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_rearWheel")
        obj.Shape=self.rearWheel
        obj.Label=self.name+"_rearWheel"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_rightFrontWheel")
        obj.Shape=self.rightFrontWheel
        obj.Label=self.name+"_rightFrontWheel"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_leftFrontWheel")
        obj.Shape=self.leftFrontWheel
        obj.Label=self.name+"_leftFrontWheel"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_frame")
        obj.Shape=self.frame
        obj.Label=self.name+"_frame"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_crank")
        obj.Shape=self.crank
        obj.Label=self.name+"_crank"
        obj.ViewObject.ShapeColor=tuple([0.5,0.5,0.5])
        obj.ViewObject.Transparency=60
        
def printTable(la,lb):
    for a,b in zip(la,lb):
        print("%6.3f,%6.3f,%6.3f|%6.3f,%6.3f,%6.3f"%(a.x,a.y,a.z,b.x,b.y,b.z),\
            file=sys.__stderr__)
        
def printIntersects(c1,c2,start,end,incrX):
    currentPoint = start
    print(incrX,file=sys.__stderr__)
    while currentPoint.x >= end.x:
        print(currentPoint,file=sys.__stderr__)
        plane = Part.makePlane(25.4,2*350,currentPoint,Base.Vector(1,0,0)).Surface
        print(c1.intersect(plane),file=sys.__stderr__)
        print(c2.intersect(plane),file=sys.__stderr__)
        currentPoint = currentPoint.add(Base.Vector(incrX,0,0))
        
class Shell(object):
    _poly1 = [(-254,347.7),(-850,0),(-254,-347.7),\
              (254,-347.7),(1700,-84),(1700,84),(254,347.7)]
    _topRibPoly = [(-850,266.7), (-254,711.2),\
                   (711.200, 711.2), (711.200, 965.2), (1700, 266.7)]
    _bottomRibPoly = [(-850,241.3), (-254,50.8),\
                      (711.200, 50.8), (1700, 241.3)]
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        polypoints = list()
        for tup in self._poly1:
            x,y = tup
            polypoints.append(origin.add(Base.Vector(x,y,254-12.7)))
        c1 = Part.BezierCurve()
        c1.setPoles([polypoints[0],polypoints[0].add(Base.Vector(-150,0,0)),\
                     polypoints[1].add(Base.Vector(-10,150,0)),polypoints[1]])
        spline = c1.toBSpline()
        c2 = Part.BezierCurve()
        c2.setPoles([polypoints[1],polypoints[1].add(Base.Vector(-10,-150,0)),\
                     polypoints[2].add(Base.Vector(-150,0,0)),polypoints[2]])
        spline.join(c2.toBSpline())
        c3 = Part.BezierCurve()
        c3.setPoles([polypoints[2],polypoints[2],polypoints[3],polypoints[3]])
        spline.join(c3.toBSpline())
        c4 = Part.BezierCurve()
        c4.setPoles([polypoints[3],polypoints[3].add(Base.Vector(150,0,0)),\
                     polypoints[4].add(Base.Vector(10,-100,0)),polypoints[4]])
        spline.join(c4.toBSpline())
        c5 = Part.BezierCurve()
        c5.setPoles([polypoints[4],polypoints[4],polypoints[5],polypoints[5]])
        spline.join(c5.toBSpline())
        c6 = Part.BezierCurve()
        c6.setPoles([polypoints[5],polypoints[5].add(Base.Vector(-10,100,0)),\
                     polypoints[6].add(Base.Vector(150,0,0)),polypoints[6]])
        spline.join(c6.toBSpline())
        c7 = Part.BezierCurve()
        c7.setPoles([polypoints[6],polypoints[6],polypoints[0],polypoints[0]])
        spline.join(c7.toBSpline())
        shape2 = Part.Face(Part.Wire(spline.toShape())).extrude(Base.Vector(0,0,25.4))
        self.shell = shape2
        toppoints = list()
        for tup in self._topRibPoly:
            x,z = tup
            toppoints.append(origin.add(Base.Vector(x,-12.7,z)))
        top_c1 = Part.BezierCurve()
        top_c1.setPoles([toppoints[0],toppoints[0].add(Base.Vector(-15,0,200)),\
                         toppoints[1].add(Base.Vector(-50,0,0)),toppoints[1]])
        topspline = top_c1.toBSpline()
        top_c2 = Part.BezierCurve()
        top_c2.setPoles([toppoints[1],toppoints[1],toppoints[2],toppoints[2]])
        topspline.join(top_c2.toBSpline())
        top_c3 = Part.BezierCurve()
        top_c3.setPoles([toppoints[2],toppoints[2],toppoints[3],toppoints[3]])
        topspline.join(top_c3.toBSpline())
        top_c4 = Part.BezierCurve()
        top_c4.setPoles([toppoints[3],toppoints[3].add(Base.Vector(100,0,0)),\
                         toppoints[4].add(Base.Vector(100,0,10)),toppoints[4]])
        topspline.join(top_c4.toBSpline())
        top_c5 = Part.BezierCurve()
        top_c5.setPoles([toppoints[4],toppoints[4],toppoints[0],toppoints[0]])
        topspline.join(top_c5.toBSpline())
        topridge = Part.Face(Part.Wire(topspline.toShape()))\
                        .extrude(Base.Vector(0,25.4,0))
        self.shell = self.shell.fuse(topridge)
        bottompoints = list()
        for tup in self._bottomRibPoly:
            x,z = tup
            bottompoints.append(origin.add(Base.Vector(x,-12.7,z)))
        bottom_c1 = Part.BezierCurve()
        bottom_c1.setPoles([bottompoints[0],bottompoints[0].add(Base.Vector(-15,0,-200)),\
                            bottompoints[1].add(Base.Vector(-50,0,0)),bottompoints[1]])
        bottomspline = bottom_c1.toBSpline()
        bottom_c2 = Part.BezierCurve()
        bottom_c2.setPoles([bottompoints[1],bottompoints[1],bottompoints[2],bottompoints[2]])
        bottomspline.join(bottom_c2.toBSpline())
        bottom_c3 = Part.BezierCurve()
        bottom_c3.setPoles([bottompoints[2],bottompoints[2].add(Base.Vector(100,0,0)),\
                            bottompoints[3].add(Base.Vector(100,0,-10)),bottompoints[3]])
        bottomspline.join(bottom_c3.toBSpline())
        bottom_c4 = Part.BezierCurve()
        bottom_c4.setPoles([bottompoints[3],bottompoints[3],bottompoints[0],bottompoints[0]])
        bottomspline.join(bottom_c4.toBSpline())
        bottomridge = Part.Face(Part.Wire(bottomspline.toShape()))\
                            .extrude(Base.Vector(0,25.4,0))
        self.shell = self.shell.fuse(bottomridge)
        #self._topRibs(c1,c2,polypoints[0],polypoints[1],(polypoints[1].x-polypoints[0].x)/5.0)
        #self._bottomRibs(c1,c2,polypoints[0],polypoints[1],(polypoints[1].x-polypoints[0].x)/5.0)
    def _topRibs(c1,c2,start,end,incrX):
        currentPoint = start
        while currentPoint.x >= end.x:
            # self._topRib(c1,c2,currentPoint,
            currentPoint = currentPoint.add(Base.Vector(incrX,0,0))
    def _topRib(self,c1,c2,currentPoint,z):
        plane = Part.makePlane(25.4,2*350,currentPoint,Base.Vector(1,0,0)).Surface
        c1intersect = c1.intersect(plane)
        c2intersect = c2.intersect(plane)
    def _bottomRibs(c1,c2,start,end,incrX):
        currentPoint = start
        while currentPoint.x >= end.x:
            # self._bottomRib(c1,c2,currentPoint,
            currentPoint = currentPoint.add(Base.Vector(incrX,0,0))
    def _bottomRib(self,c1,c2,currentPoint,z):
        plane = Part.makePlane(25.4,2*350,currentPoint,Base.Vector(1,0,0)).Surface
        c1intersect = c1.intersect(plane)
        c2intersect = c2.intersect(plane)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.shell
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,.7529,.7960])
        obj.ViewObject.Transparency=20



if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument() 
    trike = TerraTrike("trike",Base.Vector(0,0,0))
    trike.show()
    shell = Shell("shell",Base.Vector(0,0,0))
    shell.show()
    Gui.SendMsgToActiveView("ViewFit") 
    Gui.activeDocument().activeView().viewTop()  
