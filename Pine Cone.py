#pineCone.py
import maya.cmds as cmds
import functools

def createUI(pWindowTitle, pApplyCallback):
    '''
    This is a function that creates the user interface, where users can input the shape and size of petals,
    number of petals, and petal angle to create varioius pine cone like shapes
    '''
    
    windowID = 'PineCone'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    #creating UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,130), (2,60), (3,60)], columnOffset = [(1,'right',3)])
    
    #creating input fields in UI window
    cmds.text(label='Petal Shape: ')
    petalShape = cmds.optionMenu()
    cmds.menuItem(label = "Cone")
    cmds.menuItem(label = "Cylinder")
    cmds.separator(h=10,style='none')
    cmds.text(label='# Petals per Layer: ')
    numPetals = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Petal Angle: ')
    petalAngle = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Petal Height: ')
    petalHeight = cmds.floatField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Petal Radius: ')
    petalRadius = cmds.floatField()
    cmds.separator(h=10,style='none')
 
    
    #making the apply button call the applyCallback
    cmds.button(label='Apply', command=functools.partial(pApplyCallback, petalShape, numPetals, petalHeight, petalRadius, petalAngle))
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()

def applyCallback(pPetalShape, pNumPetals, pPetalHeight, pPetalRadius, pPetalAngle, *pArgs):
    '''
    This function generates pine cone like shapes from user input
    '''
    #retrieving the values from user input
    numberPetals = cmds.intField(pNumPetals, query=True,value = True)
    startH = cmds.floatField(pPetalHeight, query=True,value = True) 
    startR = cmds.floatField(pPetalRadius, query=True,value = True)
    petalAngle = cmds.intField(pPetalAngle, query=True,value = True)
    petalShape = cmds.optionMenu(pPetalShape, query=True,value = True)
    
    #creating a cone or cylinder base shape based on what the user selected from the shape dropdown menu
    if petalShape == 'Cone':
        result = cmds.polyCone(r=startR, h=startH, name ='OG#')
    else:
        result = cmds.polyCylinder(r=startR, h=startH, name ='OG#')
    
    #moving the pivot down to the base of the shape so that rotating the instances will create the radial effect
    cmds.move(0, startH/2, 0, result[0])
    cmds.move(0, 0, 0, result[0]+".scalePivot",result[0]+".rotatePivot", absolute=True)
    cmds.rotate(petalAngle,0,0, result[0])
    coneGroup = cmds.group(empty = True, name ="Group")
    
    #creating one layer with the correct number of petals
    for i in range(1,numberPetals):
            resInstance = cmds.instance(result[0], name = 'instance#')
            cmds.rotate(petalAngle, 0, 360/numberPetals*i, resInstance)
            cmds.parent(resInstance, coneGroup)
    #parenting the initial petal into this first layer
    cmds.parent(result, coneGroup) 
    
    #creating a group for all five layers
    full = cmds.group(empty = True, name ="full")
    
    #creating the other four layers
    for x in range(1,5): 
        dupInstance = cmds.instance(coneGroup, name = 'dup#') 
        cmds.move(0,0,0.2*x, dupInstance)
        #scaling each layer instance down by a larger factor each iteration
        cmds.scale(1-(0.1*x),1-(0.1*x), 1-(0.1*x), dupInstance)
        cmds.parent(dupInstance, full) 
    
    #parenting the initial layer into the final shape group
    cmds.parent(coneGroup, full) 

createUI ('Pine Cone Input', applyCallback)
       
