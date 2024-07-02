#Author-Autodesk Inc. modified by Daniel Hipp
#Description-Import coil filament coordinates from csv file and connect as spline

import adsk.core, adsk.fusion, traceback
import io
#import numpy as np

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        try:
            import numpy as np
        except:
            if ui:
                ui.messageBox('Error: numpy not installed')
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Import filament coordinates csv -> spline'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        
        dlg = ui.createFileDialog()
        dlg.title = 'Open CSV File'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return
        
        filename = dlg.filename
        '''with io.open(filename, 'r', encoding='utf-8-sig') as f:
            points = adsk.core.ObjectCollection.create()
            line = f.readline()
            data = []
            while line:
                pntStrArr = line.split(',')
                for pntStr in pntStrArr:
                    try:
                        data.append(float(pntStr))
                    except:
                        break
            
                if len(data) >= 3 :
                    point = adsk.core.Point3D.create(data[0], data[1], data[2])
                    points.add(point)
                line = f.readline()
                data.clear()'''
        #added code begin-----------------------------------
        points = adsk.core.ObjectCollection.create()
        data = np.loadtxt(filename, delimiter =',')
        datashape = np.shape(data)
        if datashape[1] != 3:
            ui.messageBox('invalid data format. Coordinates mus have shape (N,3)', title)
        x = data[:,0]
        y = data[:,1]
        z = data[:,2]
        for i in range(len(x)):
            point = adsk.core.Point3D.create(x[i], y[i], z[i])
            points.add(point)
        point = adsk.core.Point3D.create(x[0], y[0], z[0]) #create last point = first point to close the coil
        points.add(point) ##create last point = first point to close the coil
        #added code end--------------------------------------------------            
        if points.count:
            root = design.rootComponent
            sketch = root.sketches.add(root.xYConstructionPlane)
            sketch.sketchCurves.sketchFittedSplines.add(points)
        else:
            ui.messageBox('No valid points', title)            
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))