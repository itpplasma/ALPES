import cadquery as cq
from windingCoordinateGenerator import *
from tqdm import tqdm
#this is a change
#All units in mm according to Fusion360 STEP import standard
xOuter = 40 #winding pack outermost dimension in B field direction
yOuter = 67 #winding pack outermost dimension in radial direction
wallTh = 2 #Steel casing wall thickness

#--------------Prepare coil coordinates and coordinate system along the filament----------------------------------------
coilCoordList = loadAndScale('coilData\coil_coordinates0.txt', 12, 0.330*10) #*10 is to adjust scaling for step import (uses mm as basis)
CGlist = coilCG(coilCoordList)
circVecList=[]
for i, xyzCoord in enumerate(coilCoordList):
    CG = CGlist[i]
    circVec = np.cross([0,0,1],CG)# vector orthogonal to z axis and connection between z axis and CG
    circVec /= np.linalg.norm(circVec)# normalized
    circVecList.append(circVec)

X = np.asarray([1,0,0])
Y = np.asarray([0,1,0])
A = 0
B = 0

#steerVecList = []
#for i in range(12):
#    steerVecList.append(X)
steerVecList = circVecList
steerVecList[0] = Y
steerVecList[5] = Y
steerVecList[6] = Y
steerVecList[11] = Y
xDirList, yDirList, normalList = customOrientePlanes(coilCoordList, steerVecList)

#-----generate solids and associated .STEP files for the coils given in range------------------------------------------
for j in range(0,3):
    print('rendering coil #', j)
    result = None
    nextpart = None
    xDir = xDirList[j]
    ydir = yDirList[j]
    normalDir = normalList[j]
    coil = coilCoordList[j]
    for i, point2 in tqdm(enumerate(coil)):
        xvec2 = xDir[i,:]
        norm2 = normalDir[i,:]
        if i == 0:
            point1 = coil[-1,:] #last entry of list to form complete coil
            xvec1 = xDir[-1,:]
            norm1 = normalDir[-1,:]
        else:
            point1 = coil[i-1,:] #previous entry of list to loft from
            xvec1 = xDir[i-1,:]
            norm1 = normalDir[i-1,:]
        p1 = cq.Plane(origin=cq.Vector(point1[0],point1[1], point1[2]), xDir=cq.Vector(xvec1[0],xvec1[1],xvec1[2]),normal=cq.Vector(norm1[0],norm1[1],norm1[2]))
        p2 = cq.Plane(origin=cq.Vector(point2[0],point2[1], point2[2]), xDir=cq.Vector(xvec2[0],xvec2[1],xvec2[2]),normal=cq.Vector(norm2[0],norm2[1],norm2[2]))
        wp1 = cq.Workplane(p1, origin=cq.Vector(point1[0],point1[1], point1[2])).rect(xOuter,yOuter).workplane()
        wp2 = cq.Workplane(p2, origin=cq.Vector(point2[0],point2[1], point2[2])).rect(xOuter,yOuter).workplane()
        wp1.ctx.pendingWires.extend(wp2.ctx.pendingWires)
        if result == None:
            result = wp1.loft(combine=True)
        else:
            nextpart = wp1.loft(combine=True)
            result = result.union(nextpart)
    exportname = r'C:\Users\Daniel\Documents\!Privat\Physik_Master\FusionReactorDesign\CqeditorCode\CustomCoilFat'+str(j)+'.step'
    cq.exporters.export(result, exportname)
print('finished!')
#Show object when using CQ-editor
#show_object(result, options=dict(alpha=0.5,color='red'))
