import numpy as np
import random
import time

import FreeCAD
import nodeeditor.store
import Part

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.store
import nodeeditor.pfwrap as pfwrap


def runraw(self):
	# called biy FreeCAD_Object createpins
	objname=self.objname.getData()
	fobj=FreeCAD.ActiveDocument.getObject(objname)

	if fobj == None:
		print "cannot create pins because no FreeCAD object for name {}".format(objname)
		return []
	ps=fobj.PropertiesList
	if 0:
		sayl('#')
		print "FreeCAD object Properties ---"
		for p in ps:
			print p


	pins=[]
	ipm=self.namePinInputsMap

	if 0:
		print("ipm.keys() for ",objname,fobj.Name,fobj.Label)
		for k in ipm.keys():
			print k

#---------------

	recomputepins=[]
	for p in ps:
		try:
			a=getattr(fobj,p)
		except:
			print ("ignore problem with prop",p," fix it later !!")
			continue

		if p in ["Placement","Shape",
				"MapMode",
				"MapReversed","MapPathParameter",
				"Attacher",
				"AttacherType",
				"AttachmentOffset","ExpressionEngine","Support"]:
			pass
			#continue


		if p in ipm.keys():
			#print "IGNORE '{}' - exists already".format(p)
			continue

		cn=a.__class__.__name__

		if p.startswith("aLink"):
			# zu tun
			continue
#		print("################",cn,p,a)
		if cn=="list" and p.endswith('List'):

			r2=p.replace('List','Pin')
			r=r2[1:]
#			say("--------------",p,r,r2)
			if r=="IntegerPin":
				r="IntPin"
			try:
				p1 = self.createInputPin(p, r ,[],structure=PinStructure.Array)
				p2 = self.createOutputPin(p+"_out", r ,[],structure=PinStructure.Array)
				pins += [p1,p2]
			except:
				say("cannot create list pin for",p,r2)

			continue



		if cn=="Quantity" or cn=="float":
			pintyp="FloatPin"
		elif  cn=="Vector":
			pintyp="VectorPin"
		elif  cn=="str" or cn=="unicode":
			pintyp="StringPin"
		elif  cn=="bool":
			pintyp="BoolPin"
		elif  cn=="int":
			pintyp="IntPin"
		elif  cn=="Placement":
			pintyp="PlacementPin"
		elif  cn=="Rotation":
			pintyp="RotationPin"


		elif cn=='list' or cn == 'dict' or cn=='tuple' or cn=='set':
			# zu tun
			continue
		elif cn=='Material'  or cn=='Shape' or cn=='Matrix' :
			# zu tun
			continue
		elif cn=='NoneType' :
			# zu tun
			continue


		else:
			say(p,cn,a,"is not known")
			continue



		pinname=p
		pinval=a

#		say("create pin for ",pintyp,pinname,pinval)
		p1 = CreateRawPin(pinname,self, pintyp, PinDirection.Input)
		p2 = CreateRawPin(pinname+"_out",self, pintyp, PinDirection.Output)
		p1.enableOptions(PinOptions.Dynamic)
	#	p1.recomputeNode=True
		recomputepins += [p1]
		p1.setData(pinval)
		p2.setData(pinval)
		say("created:",p1)

		pins  += [p1,p2]


	sayl()

	for p in recomputepins:
		p.recomputeNode=True

	for p in pins:
		p.group="FOP"

	return pins



def run_VectorArray_compute(self,*args, **kwargs):

	countA=self.getData("countA")
	countB=self.getData("countB")
	countC=self.getData("countC")
	vO=self.getData("vecBase")
	vA=self.getData("vecA")

	vB=self.getData("vecB")
	vC=self.getData("vecC")
	rx=self.getData("randomX")
	ry=self.getData("randomY")
	rz=self.getData("randomZ")


	degA=self.getData("degreeA")
	degB=self.getData("degreeB")
	if countA<degA+1:
		degA=countA-1
	if countB<degB+1:
		degB=countB-1

	points=[vO+vA*a+vB*b+vC*c+FreeCAD.Vector((0.5-random.random())*rx,(0.5-random.random())*ry,(0.5-random.random())*rz)
		for a in range(countA) for b in range(countB) for c in range(countC)]

	if countC != 1:
		sayexc("not implemented")
		return

	if degA==0 or degB==0:
		col = []
		poles=np.array(points).reshape(countA,countB,3)
		for ps in poles:
			ps=[FreeCAD.Vector(p) for p in ps]
			col += [Part.makePolygon(ps)]
		for ps in poles.swapaxes(0,1):
			ps=[FreeCAD.Vector(p) for p in ps]
			col += [Part.makePolygon(ps)]

		shape=Part.makeCompound(col)


	else:

		poles=np.array(points).reshape(countA,countB,3)

		multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
		multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
		knotA=range(len(multA))
		knotB=range(len(multB))

		sf=Part.BSplineSurface()
		sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
		shape=sf.toShape()


	self.setData('out',poles)

	cc=self.getObject()
	try:
		cc.Label=self.objname.getData()
	except:
		pass
	cc.Shape=shape
	self.setPinObject('Shape',shape)
	self.outExec.call()







def run_Plot_compute(self,*args, **kwargs):

	import matplotlib.pyplot as plt

	if self.f2.getData():
		plt.figure(2)

	elif self.f3.getData():
		plt.figure(3)
	else:
		plt.figure(1)

#	plt.close()
	plt.title(self.getName())

	x=self.xpin.getData()
	y=self.ypin.getData()

	#say(x)
	#say(y)
	say(len(x),len(y))


	if len(y) <>0:
		N=len(y)
		if len(x)<>len(y):
			x = np.linspace(0, 10, N, endpoint=True)
		else:
			x=np.array(x)

		y=np.array(y)

		if not self.f3.getData():
			plt.plot(x, y, 'bx')
		plt.plot(x, y , 'b-')


	x2=self.xpin2.getData()
	y2=self.ypin2.getData()
	say (len(x2),len(y2))
	if x2 <> None and y2 <> None:
		x2=np.array(x2)
		y2=np.array(y2)
		if self.f3.getData():
			plt.plot(x2, y2 , 'r-')
		else:
			plt.plot(x2, y2, 'ro')


	plt.show()



def run_projection_compute(self,*args, **kwargs):

	sayl()
	f=FreeCAD.ActiveDocument.BePlane.Shape.Face1
	w=FreeCAD.ActiveDocument.Sketch.Shape.Edge1
	f=store.store().get(self.getPinN('face').getData())
	say("Face",f)
	e=store.store().get(self.getPinN('edge').getData())
	say("Edge",e)

	store.store().list()
	d=self.getPinN('direction').getData()
	say("direction",d)
	shape=f.makeParallelProjection(e,d)
	cc=self.getObject()
	if cc <> None:
		cc.Label=self.objname.getData()
		cc.Shape=shape
		#cc.ViewObject.LineWidth=8
		cc.ViewObject.LineColor=(1.,1.,0.)


def run_uv_projection_compute(self,*args, **kwargs):

	f=store.store().get(self.getPinN('face').getData())
	w=store.store().get(self.getPinN('edge').getData())
	closed=True

	sf=f.Surface

	pointcount=max(self.getPinN('pointCount').getData(),4)
	pts=w.discretize(pointcount)


	bs2d = Part.Geom2d.BSplineCurve2d()
	if closed:
		pts2da=[sf.parameter(p) for p in pts[1:]]
	else:
		pts2da=[sf.parameter(p) for p in pts]

	pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da]
	bs2d.buildFromPolesMultsKnots(pts2d,[1]*(len(pts2d)+1),range(len(pts2d)+1),True,1)
	e1 = bs2d.toShape(sf)

	sp=FreeCAD.ActiveDocument.getObject("_Spline")
	if sp==None:
		sp=FreeCAD.ActiveDocument.addObject("Part::Spline","_Spline")
	sp.Shape=e1

	face=f
	edges=e1.Edges
	ee=edges[0]
	splita=[(ee,face)]
	r=Part.makeSplitShape(face, splita)

	ee.reverse()
	splitb=[(ee,face)]
	r2=Part.makeSplitShape(face, splitb)

	try:
		rc=r2[0][0]
		rc=r[0][0]
	except: return

	cc=self.getObject()
	if cc <> None:
		cc.Label=self.objname.getData()

	if self.getPinN('inverse').getData():
		cc.Shape=r2[0][0]
	else:
		cc.Shape=r[0][0]

	if self.getPinN('Extrusion').getData():
		f = FreeCAD.getDocument('project').getObject('MyExtrude')
		if f == None:
			f = FreeCAD.getDocument('project').addObject('Part::Extrusion', 'MyExtrude')

		f.Base = sp
		f.DirMode = "Custom"
		f.Dir = FreeCAD.Vector(0.000000000000000, 0.000000000000000, 1.000000000000000)
		f.LengthFwd = self.getPinN('ExtrusionUp').getData()
		f.LengthRev = self.getPinN('ExtrusionDown').getData()
		f.Solid = True
		FreeCAD.activeDocument().recompute()

	#see without extra part >>> s.Face1.extrude(FreeCAD.Vector(0,1,1))
	#<Solid object at 0x660e520>


def run_Bar_compute(self,*args, **kwargs):
	sayl()


def run_Foo_compute(self,*args, **kwargs):
	sayl()



def run_enum(self):
	say("process the rawPin data ")
	say("rawPin is",self.pin._rawPin)
	say("values ...")
	for v in self.pin._rawPin.values:
		say(v)



def f4(self):
	say("FreeCAD Ui Node runs f4")
	say("nothing to do, done")

import FreeCADGui

def run_view3d(self,name,shape,workspace,mode,wireframe,transparency):
	
	#sayl()


	shape=self.getPinObject('Shape')
	s=shape
	l=FreeCAD.listDocuments()
	if workspace=='' or workspace=='None':
		w=l['Unnamed']
	else:
		if workspace in l.keys():
			w=l[workspace]
		else:
			w=FreeCAD.newDocument(workspace)

			#Std_CascadeWindows
			FreeCADGui.runCommand("Std_ViewDimetric")
			FreeCADGui.runCommand("Std_ViewFitAll")
			FreeCADGui.runCommand("Std_TileWindows")

	#s=store.store().get(shape)

	f=w.getObject(name)
	if f == None:
		f = w.addObject('Part::Feature', name)
	if s <> None:
		f.Shape=s
	#say("shape",s);say("name",name)

	w.recompute()

	if not wireframe:
		f.ViewObject.DisplayMode = "Flat Lines"
		f.ViewObject.ShapeColor = (random.random(),random.random(),1.)
	else:
		f.ViewObject.DisplayMode = "Wireframe"
		f.ViewObject.LineColor = (random.random(),random.random(),1.)

	#f.ViewObject.Transparency = transparency




from PyFlow.Packages.PyFlowBase.Factories.UINodeFactory import createUINode


def run_foo_compute(self,*args, **kwargs):
	pass


def run_visualize(self,*args, **kwargs):
	say(self._rawNode)
	say("create vid3d object in graph")
	gg=self.graph()
	x,y=-150,-100
	nodeClass='FreeCAD_view3D'
	#t3 = pfwrap.createNode('PyFlowFreeCAD',nodeClass,"MyPolygon")
	#t3.setPosition(x,y)
	#gg.addNode(t3)
	#uinode=createUINode(t3)
	#say(uinode)
	aa=self.canvasRef().spawnNode(nodeClass, x, y)
	say(aa.__class__)
	say("connect Shape withj vie3d.shape ...")
	FreeCAD.aa=aa
	pfwrap.connect(self._rawNode,'Shape',aa._rawNode,'Shape')
	sayl()

	pfwrap.connect(self._rawNode,'outExec',aa._rawNode,'inExec')
	aa._rawNode.setData('name','View_'+self._rawNode.name)




def run_FreeCAD_Tripod(self,*args, **kwargs):
	sayl()
	f=self.getPinObject('Shape')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	#if f.__class__.__name__  == 'Face':
	
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	say(umin,umax,vmin,vmax)
	u,v=self.getData("u"),self.getData("v")
	
	say(f)
	uu=umin+(umax-umin)*0.1*u
	vv=vmin+(vmax-vmin)*0.1*v
	pos=sf.value(uu,vv)
	self.setData('position',pos)
	
	if self.getData('curvatureMode'): 
		# curvature
		t1,t2=sf.curvatureDirections(uu,vv)


	else: # tangents
		t1,t2=sf.tangent(uu,vv)
#		t1=t1.normalize()
#		t2=t2.normalize()

	if self.getData('directionNormale'): 
			n=t1.cross(t2).normalize()
	else: 
			n=t2.cross(t1).normalize()

	
	if self.getData('display'):
		obj=self.getObject()
		shape=Part.makePolygon([pos,pos+t1*10,pos+t2*5,pos,pos+n*5],
						)
		obj.Shape=shape


	self.outExec.call()



def run_FreeCAD_uIso(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	u=self.getData("u")

	uu=umin+(umax-umin)*0.1*u
	c=sf.uIso(uu)
	self.setPinObject('Edge',c.toShape())

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=c.toShape()

	self.outExec.call()


def run_FreeCAD_vIso(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	v=self.getData("v")

	vv=vmin+(vmax-vmin)*0.1*v
	c=sf.vIso(vv)
	self.setPinObject('Edge',c.toShape())

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=c.toShape()

	self.outExec.call()

def run_FreeCAD_uvGrid(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	uc=self.getData("uCount")
	vc=self.getData("vCount")
	
	us=[]
	for u in range(uc+1):
		uu=umin+(umax-umin)*u/uc
		c=sf.uIso(uu).toShape()
		us += [c]

	vs=[]
	for v in range(vc+1):
		vv=vmin+(vmax-vmin)*v/vc
		c=sf.vIso(vv).toShape()
		vs += [c]

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=Part.Compound(us+vs)

	self.setPinObjects('uEdges',us)
	self.setPinObjects('vEdges',vs)



def check(xa,ya,xb,yb):
	return (0<=xa and xa<=1) and (0<=ya and ya<=1) and (0<=xb and xb<=1) and (0<=yb and yb<=1)

def trim(xa,ya,xb,yb):
	if xa<0:
		t=-xb/(xa-xb)
		xa2=0
		ya2=t*ya+(1-t)*yb
		return (xa2,ya2,xb,yb)
	if xa>1:
		t=(1-xb)/(xa-xb)
		xa2=1
		ya2=t*ya+(1-t)*yb
		return (xa2,ya2,xb,yb)

	if ya<0:
		t=-yb/(ya-yb)
		ya2=0
		xa2=t*xa+(1-t)*xb
		return (xa2,ya2,xb,yb)
	if ya>1:
		t=(1-yb)/(ya-yb)
		ya2=1
		xa2=t*xa+(1-t)*xb
		return (xa2,ya2,xb,yb)

	if xb<0:
		t=-xa/(xb-xa)
		xb2=0
		yb2=t*yb+(1-t)*ya
		return (xa,ya,xb2,yb2)
	if xb>1:
		t=(1-xa)/(xb-xa)
		xb2=1
		yb2=t*yb+(1-t)*ya
		return (xa,ya,xb2,yb2)

	if yb<0:
		t=-ya/(yb-ya)
		yb2=0
		xb2=t*xb+(1-t)*xa
		return (xa,ya,xb2,yb2)
	if yb>1:
		t=(1-ya)/(yb-ya)
		yb2=1
		xb2=t*xb+(1-t)*xa
		return (xa,ya,xb2,yb2)


	return xa,ya,xb,yb



def mapEdgesLines( uvedges,face):

	col=[]
	umin,umax,vmin,vmax=face.ParameterRange
	sf=face.Surface
	for edge in uvedges:
		ua,va,ub,vb=edge
		ua=umin+ua*(umax-umin)
		va=vmin+va*(vmax-vmin)

		ub=umin+ub*(umax-umin)
		vb=vmin+vb*(vmax-vmin)
		
		pa=sf.value(ua,va)
		pb=sf.value(ub,vb)
		say(pa)
		col += [Part.makePolygon([pa,pb])]

	shape=Part.Compound(col)
	return shape

def mapEdgesCurves( edges,face):
	'''geschmiegte V<ariante'''

	col=[]
	umin,umax,vmin,vmax=face.ParameterRange
	sf=face.Surface
	for edge in edges:
		ua,va,ub,vb=edge
		ua=umin+ua*(umax-umin)
		va=vmin+va*(vmax-vmin)
		ub=umin+ub*(umax-umin)
		vb=vmin+vb*(vmax-vmin)

		a=FreeCAD.Base.Vector2d(ua,va)
		b=FreeCAD.Base.Vector2d(ub,vb)
		bs2d = Part.Geom2d.BSplineCurve2d()
		bs2d.buildFromPolesMultsKnots([a,b],[2,2],[0,1],False,1)
		ee = bs2d.toShape(sf)
		col += [ee]

	shape=Part.Compound(col)
	return shape

def mapPoints(pts,face):
	'''create subface patch boundet by pts on face'''

	umin,umax,vmin,vmax=face.ParameterRange
	sf=face.Surface

	say("DEBUG---------------") # hier ist noch verfeinerugn noetig
	if 0:
		ptsn=[]
		for p in pts:
			if p.x<0:
				p.x=0.00001
			if p.x>1:
				p.x=0.99999
			if p.y<0:
				p.y=0.00001
			if p.y>1:
				p.y=0.99999
				
			ptsn += [p]
		pts=ptsn

	col=[]
	for p in pts:
		ua,va = p[0],p[1]
		ua=umin+ua*(umax-umin)
		va=vmin+va*(vmax-vmin)
		a=FreeCAD.Base.Vector2d(ua,va)
		col += [a]
	col += [col[0]] # close curve

	bs2d = Part.Geom2d.BSplineCurve2d()
	ms=[2]+[1]*(len(col)-2)+[2]
	ks=range(len(ms))
	bs2d.buildFromPolesMultsKnots(col,ms,ks,False,1)
	eee = bs2d.toShape(sf)

	edge=eee.Edges[0]
	splita=[(edge,face)]
	r=Part.makeSplitShape(face, splita)

	edge.reverse()
	splitb=[(edge,face)]
	r2=Part.makeSplitShape(face, splitb)

	shapes=[]

	try:
		shapes += [r2[0][0]]
	except:
		pass
	try:
		shapes += [rc]
	except:
		pass

	shapes += [eee]

	return shapes



def run_FreeCAD_Voronoi(self,*args, **kwargs):
	'''
	create voronoi and delaunay stuff using scipy, see
	https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.spatial.Voronoi.html
	'''

	from scipy.spatial import Voronoi, voronoi_plot_2d

	# get data from inpins or generate somthinfg for testing
	face=self.getPinObject("Face")
	ulist=self.getData("uList")
	vlist=self.getData("vList")

	if len(ulist) == len(vlist) and len(ulist)>0:
		say("use old")
		pointsa=zip(ulist,vlist)
	else:
		say("ewigene datan")
		n=30
		try: 
			pointsa=self.pointsa
			#1/0
		except:
			pointsa=np.random.random(2*n).reshape(n,2)*0.8 + [0.1,0.1]
			self.pointsa=pointsa

	# add the bounding box in normalized uvspace
	points = np.concatenate([pointsa,np.array([[0,0],[0,1],[1,0],[1,1]])])

	# core calculation
	vor = Voronoi(points)
	points=[FreeCAD.Vector(v[0],v[1]) for v in points]

	if 0:
		say("ridge points--")
		say(len(vor.ridge_points))
		say(vor.ridge_points)


	#
	# delaunay
	#
	edges=[]
	col=[]
	for r in  vor.ridge_points:
		pts=[points[v] for v in r if v <> -1]
		if len(pts)>1:
			for i in range(len(pts)-1):
				pa=pts[i]
				pb=pts[i+1]
				xa,ya=pa[0],pa[1]
				xb,yb=pb[0],pb[1]
				edges += [(xa,ya,xb,yb)]

	if self.getData("useLines"):
		shape=mapEdgesLines(edges,face)
	else:
		shape=mapEdgesCurves(edges,face)

	spoints=[v.Point for v in shape.Vertexes]
	self.setPinObject("delaunayTriangles",shape)

	#
	# voronoi 
	#
	vertexes=[FreeCAD.Vector(v[0],v[1]) for v in vor.vertices]

	if 0:
		say("regions")
		say(vor.regions)

		say("point region")
		say(vor.point_region)

		say("ridge_vertexes")
		say(vor.ridge_vertices)

	col=[]
	col2=[]
	uvedges=[]
	#for r in  vor.regions:
	say("ridge_vertices ..")
	pos=self.getData('indA')
	#
	# this code is buggy !!!
	#
	#for ix, r in  enumerate(vor.ridge_vertices):
	for ix, r in  enumerate(vor.regions):
		pts=[vertexes[v] for v in r if v <> -1]
		say(ix,len(r),len(pts))
		#if ix <>pos:
		#	continue
		uvedgesA=[]
		if len(pts)>1:
			col += [Part.makePolygon(pts)]
			for i in range(len(pts)-1):
				pa=pts[i]
				pb=pts[i+1]
				xa,ya=pa[0],pa[1]
				xb,yb=pb[0],pb[1]
				
				if not check (xa,ya,xb,yb):
					(xa,ya,xb,yb)=trim(xa,ya,xb,yb)
				if check (xa,ya,xb,yb):
					pa=FreeCAD.Vector(xa,ya)
					pb=FreeCAD.Vector(xb,yb)
					say()
					uvedges += [(xa,ya,xb,yb)]
					uvedgesA += [(xa,ya,xb,yb)]
					#col2 += [Part.makePolygon([pa,pb])]
				if not check (xa,ya,xb,yb):
					(xa,ya,xb,yb)=trim(xa,ya,xb,yb)
					if check (xa,ya,xb,yb):
						pa=FreeCAD.Vector(xa,ya)
						pb=FreeCAD.Vector(xb,yb)
						say()
						#uvedges += [(xa,ya,xb,yb)]
						uvedgesA += [(xa,ya,xb,yb)]
						#col2 += [Part.makePolygon([pa,pb])]
					else:
						say("Err",xa,ya,xb,yb)
		try:
			uuu=uvedgesA+[(uvedgesA[-1][2],uvedgesA[-1][3],uvedgesA[0][0],uvedgesA[0][1])]
			say(uuu[0])
			say(uuu[-1])
			say("--")
		except:
			pass

	# create the output shape
	if self.getData("useLines"):
		shape=mapEdgesLines(uvedges,face)
	else:
		shape=mapEdgesCurves(uvedges,face)
	self.setPinObject("voronoiCells",shape)


#-------------------volle zellen

	#
	# regions filled 
	#
	say("vor.regions",vor.regions)
	for ix, r in  enumerate(vor.regions):
		pts=[vertexes[v] for v in r if v <> -1]
		if ix==self.getData('indA'):
			say(ix,r)
			if len(pts)<=2:
				say("zuwenig punkte")
			else:
				shapes=mapPoints(pts,face)

				cc=FreeCAD.ActiveDocument.getObject("regionFilled")
				if cc == None:
					cc=FreeCAD.ActiveDocument.addObject("Part::Feature","regionFilled")
				cc.Shape=shapes[0]
				if self.getData('flipArea'):
					say(shapes)
					cc.Shape=shapes[1]
			break





	from scipy.spatial import Delaunay

	tri = Delaunay(pointsa)
	say(tri.simplices)
	points=[FreeCAD.Vector(p[0],p[1]) for p in points]

	#
	# simplexes
	#
	if 0:
		coll=[]
		if 0: # 3D Variante
			for s in tri.simplices:
				[a,b,c,d]=s
				a=points[a]
				b=points[b]
				c=points[c]
				d=points[d]
				coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([a,d]),Part.makePolygon([b,c]),Part.makePolygon([b,d]),Part.makePolygon([c,d])]
		else: #2 D
			for s in tri.simplices:
				[a,b,c]=s
				a=points[a]
				b=points[b]
				c=points[c]
				coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([b,c])]

	#
	# convex hull
	#
#	coll=[]
	edges=[]
	for s in tri.convex_hull:
		[a,b]=s
		a=points[a]
		b=points[b]
#		coll += [Part.makePolygon([a,b])]
		xa,ya=a[0],a[1]
		xb,yb=b[0],b[1]
		edges += [(xa,ya,xb,yb)]

	if self.getData("useLines"):
		shape=mapEdgesLines(edges,face)
	else:
		shape=mapEdgesCurves(edges,face)
	self.setPinObject("convexHull",shape)

	#
	# punkte veranschaulichen
	#
	col=[]
	for p in spoints:
		col += [Part.makeSphere(50,p)]

	shape=Part.Compound(col)
	self.setPinObject("Points",shape)


	self.outExec.call()




def run_FreeCAD_Hull(self,*args, **kwargs):
	'''
	calculate voronoi delaunay  stuff for 3D point cloud
	'''

	from scipy.spatial import Delaunay

	# get the point cloud
	shape=self.getPinObject("Shape")
	points=[v.Point for v in shape.Vertexes]

	# threshold parameter for alpha hull
	lmax=0.03*(self.getData('alpha')+0.1)

	#core calculation
	atime=time.time()
	tri = Delaunay(points)
	say("time to caculate delaunay:{}".format(time.time()-atime)) 

	# say(tri.simplices)

	#
	# simplexes and alpha hull
	#
	atime=time.time()
	coll=[]
	colf=[]

	for s in tri.simplices:
		aatime=time.time()
		[a,b,c,d]=s
		a=points[a]
		b=points[b]
		c=points[c]
		d=points[d]
		coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([a,d]),Part.makePolygon([b,c]),Part.makePolygon([b,d]),Part.makePolygon([c,d])]

		bbtime=time.time()
		tta=Part.makePolygon([a,b,c,a]).Edges
		ttb=Part.makePolygon([a,b,d,a]).Edges
		ttc=Part.makePolygon([a,c,d,a]).Edges
		ttd=Part.makePolygon([b,c,d,b]).Edges

		# create a alpha simplex if it is small enough 
		if max ([e.Length for e in tta+ttb+ttc+ttd])<lmax:
			bbtime=time.time()

			w=Part.BSplineSurface()
			w.buildFromPolesMultsKnots(np.array([[a,b],[a,c]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
			colf += [w.toShape()]
			w.buildFromPolesMultsKnots(np.array([[a,b],[a,d]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
			colf += [w.toShape()]
			w.buildFromPolesMultsKnots(np.array([[b,c],[b,d]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
			colf += [w.toShape()]
			w.buildFromPolesMultsKnots(np.array([[a,d],[a,c]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
			colf += [w.toShape()]
#			say("! time alpha:makefaces {}  simplex edges{}".format(time.time()-bbtime,bbtime-aatime)) 
	say("time to caculate alpha:{}".format(time.time()-atime)) 


	# restrict set if simplexes is flag simpleSimplex is set
	atime=time.time()
	if self.getData('singleSimplex'):
		index=self.getData('simplex')
		coll=coll[6*index:6*index+6]

	shape=Part.Compound(coll)
	self.setPinObject("delaunayTriangles",shape)

	try:
		shape=Part.Compound(colf)
	except:
		shape=Part.Shape()
	if len(colf)==0:
		shape=Part.makeSphere(0.0)

	self.setPinObject("alphaHull",shape)
	say("number of bordercells",len(colf)/3)

	#
	# convex hull
	#
	coll=[]
	for s in tri.convex_hull:
		[a,b,c]=s
		a=points[a]
		b=points[b]
		c=points[c]
		coll += [Part.makePolygon([a,b]),Part.makePolygon([b,c]),Part.makePolygon([c,a])]

	self.setPinObject("convexHull",Part.Compound(coll))

	# post process following nodes
	atime=time.time()
	self.outExec.call()
	say("time for call view3dNodes:{}".format(time.time()-atime)) 
