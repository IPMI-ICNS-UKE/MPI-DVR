"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""
# External libraries
import vtk
import numpy as np



class vtk_pipeline:
    def __init__(self):
        # Defintion of visualization parameters 
        self.op_max_bl = 0.5
        self.op_max_rm = 0.5
        self.th_bl = 0.0
        self.th_rm = 0.0
        self.ri_bl = 1.0
        self.ri_rm = 1.0
        self.min_value = 0.0
        self.max_value = 0.1
        self.dimensions_vtk_data = [50, 50, 50]
        self.spacing_vtk_data = [0.1, 0.1, 0.1]
        
        self.scale_factor = 1.0          

        # bl parameters 
        self.blAmbient = 0.4
        self.blDiffuse = 0.5
        self.blSpecular = 0.05

        # rm parameters        
        self.image_data_rm = self.createEmptyImageData()
        
        self.rmAmbient = 0.4
        self.rmDiffuse = 0.5 
        self.rmSpecular = 0.05        
        self.cutoff_factor_rm = 0.05  
        
        # Color map and scalar bar parameters
        self.height_scalarBar = 250        
        self.HSV_color_max_value = 0, 1.0, 1.0
        self.HSV_color_min_value = 0.166, 1.0, 1.0    
        
        # Saclar bar bools
        self.bool_scalar_bar_bl = False
        self.bool_scalar_bar_rm = False
        
        # Maunal lookup table        
        self.lookup_table_matrix = []         
         
        # VTK writer to save mha rm file
        self.writer_rm = vtk.vtkMetaImageWriter()            
        
        # Setup of 3D visualization pipeline        
        empty_image_bl = self.createEmptyImageData()
        empty_image_rm = self.createEmptyImageData()   
        self.grid_volume = self.createGrid()
        
        self.volumeMapperBl = vtk.vtkGPUVolumeRayCastMapper()    
        self.volumeMapperBl.SetInputData(empty_image_bl)
        
        self.volumeMapperRm = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeMapperRm.SetInputData(empty_image_rm)        
        
        # Placeholder lookup tables are created
        placeholderOpTransferFunctionBl = self.createLookupTableSlider( 'bl')        
        placeholderOpTransferFunctionRm = self.createLookupTableSlider( 'rm')        

        
        volumeGradientOpBl = vtk.vtkPiecewiseFunction()
        volumeGradientOpBl.AddPoint(0.0,   0.2)
        volumeGradientOpBl.AddPoint(0.080,  0.5)
        volumeGradientOpBl.AddPoint(0.100, 0.8)
        
        volumeGradientOpRm = vtk.vtkPiecewiseFunction()
        volumeGradientOpRm.AddPoint(0,   0.2)
        volumeGradientOpRm.AddPoint(0.080,  0.5)
        volumeGradientOpRm.AddPoint(0.100, 0.8)

        
        self.volumePropertyBl = vtk.vtkVolumeProperty()        
        self.volumePropertyBl.SetScalarOpacity(placeholderOpTransferFunctionBl)
        self.volumePropertyBl.ShadeOn()
        self.volumePropertyBl.SetInterpolationTypeToLinear()
        self.volumePropertyBl.SetAmbient(self.blAmbient)
        self.volumePropertyBl.SetDiffuse(self.blDiffuse)
        self.volumePropertyBl.SetSpecular(self.blSpecular) 
        self.volumePropertyBl.SetGradientOpacity(volumeGradientOpBl)   
        
        
        self.volumePropertyRm = vtk.vtkVolumeProperty()        
        self.volumePropertyRm.SetScalarOpacity(placeholderOpTransferFunctionRm)
        self.volumePropertyRm.ShadeOn()              
        self.volumePropertyRm.SetInterpolationTypeToLinear()
        self.volumePropertyRm.SetAmbient(self.rmAmbient)
        self.volumePropertyRm.SetDiffuse(self.rmDiffuse)
        self.volumePropertyRm.SetSpecular(self.rmSpecular)
        self.volumePropertyRm.SetGradientOpacity(volumeGradientOpRm) 
                     
        self.volume_bl = vtk.vtkVolume()
        self.volume_bl.SetMapper(self.volumeMapperBl)
        self.volume_bl.SetProperty(self.volumePropertyBl)          
        
        self.volume_rm = vtk.vtkVolume()
        self.volume_rm.SetMapper(self.volumeMapperRm)
        self.volume_rm.SetProperty(self.volumePropertyRm)   
        
        # Creation of additional 2D actors to be visualized   
        # 1. Scalar bars to visualize color map range
        self.actor_scalar_bar_bl = self.createColorScalarBar(0.0, 1.0)
        self.actor_scalar_bar_rm = self.createColorScalarBar(0.0, 1.0)            
           
        # 2. Text actor to display camera position and focal point
        self.text_actor = vtk.vtkTextActor()                
        self.text_actor.SetPosition ( 20, 20 )
        self.text_actor.GetTextProperty().SetFontSize (24 )
        self.text_actor.GetTextProperty().SetColor ( 0.8, 0.8, 0.8 )
        self.text_actor.GetTextProperty().SetOpacity ( 0.8)    
        
        # Setup renderer
        self.ren = vtk.vtkRenderer()   
        self.ren.AddVolume(self.volume_rm)
        self.ren.AddVolume(self.volume_bl)        
        self.ren.AddActor2D (self.text_actor )        
        self.ren.SetBackground(1.0,1.0,1.0)
        self.ren.ResetCamera()        

    
    def updateRampIntervallBl(self, ri_bl):    
        self.ri_bl = ri_bl
        self.volumePropertyBl.SetScalarOpacity(self.createLookupTableSlider( 'bl'))    
        self.iren.Initialize()
        self.iren.Start()        
        
    def updateRampIntervallRm(self, ri_rm):   
        self.ri_rm = ri_rm
        self.volumePropertyRm.SetScalarOpacity(self.createLookupTableSlider('rm'))      
        self.iren.Initialize()
        self.iren.Start()    
    
    def updateThBl(self, th_bl):     
        self.th_bl = th_bl
        self.volumePropertyBl.SetScalarOpacity(self.createLookupTableSlider('bl'))      
        self.iren.Initialize()
        self.iren.Start()
        
    def updateThRm(self, th_rm):  
        self.th_rm = th_rm       
        self.volumePropertyRm.SetScalarOpacity(self.createLookupTableSlider('rm'))        
        self.iren.Initialize()
        self.iren.Start()          
            
    def updateOpRm(self, op_max_rm):  
        self.op_max_rm = op_max_rm
        self.volumePropertyRm.SetScalarOpacity(self.createLookupTableSlider('rm'))   
        self.iren.Initialize()
        self.iren.Start()    
        
    def updateOpBl(self, op_max_bl):   
        self.op_max_bl = op_max_bl     
        self.volumePropertyBl.SetScalarOpacity(self.createLookupTableSlider('bl'))   
        self.iren.Initialize()
        self.iren.Start()        
        
    def linearRampFunction(self, variable_ending, x):
        op_max_string = 'self.op_max_' + variable_ending        
        op_max = eval(op_max_string)        
        ri_string = 'self.ri_' + variable_ending 
        ri = eval(ri_string)        
        th_string = 'self.th_' + variable_ending 
        th = eval(th_string)       

        # Compute function parameters of linear ramp curve (f(x)= m*x + d)        
        m = op_max / ri
        d = -1.0 * th * m        
        return m * x + d              
        
    def createGrid(self):        
        imageDataGrid = vtk.vtkImageData()
        
        x_grid = self.spacing_vtk_data[0] * (self.dimensions_vtk_data[0]-1)
        y_grid = self.spacing_vtk_data[1] * (self.dimensions_vtk_data[1]-1)
        z_grid = self.spacing_vtk_data[2] * (self.dimensions_vtk_data[2]-1)         
        
        imageDataGrid.SetDimensions(2,2,2)        
        imageDataGrid.SetSpacing(x_grid, y_grid, z_grid)   
        
        volumeMapperGrid =  vtk.vtkDataSetMapper()  
        volumeMapperGrid.SetInputData(imageDataGrid)
        
        actorGrid = vtk.vtkActor()
        actorGrid.SetMapper(volumeMapperGrid)
        actorGrid.GetProperty().SetRepresentationToWireframe()
        actorGrid.GetProperty().SetOpacity(1.0)
        actorGrid.GetProperty().SetColor(0.0, 0.0, 0.0)        
        return actorGrid            
        
    def createLookupTableSlider(self, name):
        """ 
        This function creates a lookup table based on the 
        visualization parameters that can be dynamically changed using 
        the sliders. 
        """
        opTransferFunction = vtk.vtkPiecewiseFunction()          
               
        if (name == 'bl'):        
            x_increment = self.ri_bl / 10.0
            x_start = self.th_bl
            x_end = self.th_bl + self.ri_bl + x_increment
            x_plateau = self.th_bl + 2.0 *self.ri_bl
            
            for x in np.arange(x_start, x_end, x_increment):
                opTransferFunction.AddPoint(x, self.linearRampFunction('bl',x))
            # Add plateau after ramp
            opTransferFunction.AddPoint(x_plateau, self.op_max_bl)            
        
        if (name == 'rm'): 
            x_increment = self.ri_rm / 10.0
            x_start = self.th_rm
            x_end = self.th_rm + self.ri_rm + x_increment
            x_plateau = self.th_rm + 2.0 *self.ri_rm
            
            for x in np.arange(x_start, x_end, x_increment):
                opTransferFunction.AddPoint(x, self.linearRampFunction('rm',x))
            # Add plateau after ramp
            opTransferFunction.AddPoint(x_plateau, self.op_max_rm)
            
        return opTransferFunction    
    
    def createLookupTableFromManualInput(self): 
        opTransferFunction = vtk.vtkPiecewiseFunction()
        
        for i in range(len([row[0] for row in self.lookup_table_matrix])):
            opTransferFunction.AddPoint(self.lookup_table_matrix[i][0], \
                            self.lookup_table_matrix[i][1])
            
        return opTransferFunction     
    
    def updateVTKparameters(self, dim_images, spacing_images):         
        self.volumePropertyBl.SetScalarOpacity(self.createLookupTableSlider('bl')) 
        self.volumePropertyRm.SetScalarOpacity(self.createLookupTableSlider('rm')) 

        self.setMonoColor('bl', 1, 0, 0)
        self.setMonoColor('rm', 0, 0, 1)       
        
        # Update dimensions of visualized dataset
        self.dimensions_vtk_data = dim_images        
        self.spacing_vtk_data = spacing_images
        
        # Create new grid with updated size 
        self.actor_grid = self.createGrid()
        
        # Clear road-map, if new dataset is loaded 
        self.clearRm()
    
    def setMonoColor(self, name, r, g, b):
        colorTransferFunction = vtk.vtkColorTransferFunction()        
        colorTransferFunction.AddRGBPoint(0,r,g,b)
        
        if name == 'bl': 
            self.volumePropertyBl.SetColor(colorTransferFunction)
        if name == 'rm':
            self.volumePropertyRm.SetColor(colorTransferFunction)
            
        self.iren.Initialize()
        self.iren.Start()    
    
    def createColorLookupTable(self, min_value, max_value):
        colorTransferFunctionbl = vtk.vtkColorTransferFunction()
        colorTransferFunctionbl.SetColorSpaceToHSV()
        colorTransferFunctionbl.AddHSVPoint(min_value, \
            self.HSV_color_min_value[0], self.HSV_color_min_value[1], \
            self.HSV_color_min_value[2])
        colorTransferFunctionbl.AddHSVPoint(max_value, \
            self.HSV_color_max_value[0], self.HSV_color_max_value[1], \
            self.HSV_color_max_value[2]) 
        
        # Activate above / below range color, in default 
        # below range = yellow, above range = red
        #print(colorTransferFunctionbl.GetAboveRangeColor())
        #print(colorTransferFunctionbl.GetBelowRangeColor())        
        #colorTransferFunctionbl.UseBelowRangeColorOn ()
        #colorTransferFunctionbl.UseAboveRangeColorOn ()        
        return colorTransferFunctionbl
    
    def updateColorMap(self, name, min_value, max_value):
        colorTransferFunction = self.createColorLookupTable(min_value, max_value)
        if name == 'bl':
            self.volumePropertyBl.SetColor(colorTransferFunction)
        if name == 'rm':
            self.volumePropertyRm.SetColor(colorTransferFunction)
        self.iren.Initialize()
        self.iren.Start()
    
    def createColorScalarBar(self, min_value, max_value): 
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange (min_value, max_value)
        hueLut.SetHueRange (self.HSV_color_min_value[0], self.HSV_color_max_value[0])
        hueLut.SetSaturationRange (self.HSV_color_min_value[1], self.HSV_color_max_value[1])
        hueLut.SetValueRange (self.HSV_color_min_value[2], self.HSV_color_max_value[2])
        hueLut.Build()
        
        scalarBar = vtk.vtkScalarBarActor()        
        scalarBar.SetLookupTable(hueLut)
        scalarBar.SetTitle('')
        scalarBar.SetPosition(0.03, 0.12)
        scalarBar.SetNumberOfLabels(2)
        scalarBar.GetLabelTextProperty().SetColor ( 0.8, 0.8, 0.8 )
        scalarBar.SetMaximumHeightInPixels (self.height_scalarBar)
        scalarBar.GetLabelTextProperty().SetOpacity ( 0.2)
                
        return scalarBar
    
    def updateScalarBar(self, name, min_value, max_value): 
        if name == 'bl':
            self.ren.RemoveActor2D(self.actor_scalar_bar_bl)
            self.actor_scalar_bar_bl = self.createColorScalarBar(min_value, max_value)
            self.actor_scalar_bar_bl.SetTitle ('Bolus')
            self.actor_scalar_bar_bl.SetUnconstrainedFontSize(True)	
            self.actor_scalar_bar_bl.GetTitleTextProperty().SetColor(0.8, 0.8, 0.8)            
            self.actor_scalar_bar_bl.GetTitleTextProperty().SetFontSize(26)
            self.actor_scalar_bar_bl.GetTitleTextProperty().ItalicOff ()
            self.actor_scalar_bar_bl.GetTitleTextProperty().BoldOff ()
            self.actor_scalar_bar_bl.SetVerticalTitleSeparation(20)
            self.actor_scalar_bar_bl.SetTextPositionToPrecedeScalarBar()	
            self.actor_scalar_bar_bl.GetLabelTextProperty().SetFontSize(20)

            if self.bool_scalar_bar_rm == True:
                self.actor_scalar_bar_bl.SetPosition(0.03, 0.5)            
            self.ren.AddActor2D(self.actor_scalar_bar_bl)
            
        if name == 'rm':
            self.ren.RemoveActor2D(self.actor_scalar_bar_rm)        
            self.actor_scalar_bar_rm = self.createColorScalarBar(min_value, max_value) 
            self.actor_scalar_bar_rm.SetTitle ('Roadmap')    
            self.actor_scalar_bar_rm.SetUnconstrainedFontSize(True)	
            self.actor_scalar_bar_rm.GetTitleTextProperty().SetColor(0.8, 0.8, 0.8)            
            self.actor_scalar_bar_rm.GetTitleTextProperty().SetFontSize(26)
            self.actor_scalar_bar_rm.GetTitleTextProperty().ItalicOff ()
            self.actor_scalar_bar_rm.GetTitleTextProperty().BoldOff () 
            self.actor_scalar_bar_rm.SetTextPositionToPrecedeScalarBar()	
            self.actor_scalar_bar_rm.SetVerticalTitleSeparation(20)	
            self.actor_scalar_bar_rm.GetLabelTextProperty().SetFontSize(20)

            if self.bool_scalar_bar_bl == True:
                self.actor_scalar_bar_rm.SetPosition(0.03, 0.5)
            self.ren.AddActor2D(self.actor_scalar_bar_rm)  
        
       
    def rmBuildup(self, current_image_data):
        self.image_data_rm.SetSpacing(current_image_data.GetSpacing())
                         
        self.image_data_new_rm = vtk.vtkImageData()        
        self.image_data_new_rm.SetDimensions(current_image_data.GetDimensions()[0], \
                 current_image_data.GetDimensions()[1],  \
                 current_image_data.GetDimensions()[2])        
        self.image_data_new_rm.AllocateScalars(vtk.VTK_DOUBLE, 1)            
        self.image_data_new_rm.SetSpacing(current_image_data.GetSpacing())              
        
        # Compute cutoff value to eliminate background noise contribution to rm
        cutoff_rm_buildup = self.min_value + self.cutoff_factor_rm \
                                 * (self.max_value -self.min_value)           
            
        for z in range(current_image_data.GetDimensions()[2]):
            for y in range(current_image_data.GetDimensions()[1]):
                for x in range(current_image_data.GetDimensions()[0]):
                    
                    value_rm = self.image_data_rm.GetScalarComponentAsDouble(x,y,z,0)
                    value_current_image = current_image_data.GetScalarComponentAsDouble(x, y, z, 0)
                    if value_current_image > cutoff_rm_buildup:
                        """ 
                        For the Rm buildup highest value of 
                        rm matrix is compared to highest value 
                        of current image data. Other build up
                        functions can be implemented here.
                        """                                                
                        new_value = max({value_current_image, value_rm})                          
                        self.image_data_rm.SetScalarComponentFromDouble(x,y,z,0,new_value)
                        
                    new_value_rm = self.image_data_rm.GetScalarComponentAsDouble(x,y,z,0)    
                    self.image_data_new_rm.SetScalarComponentFromDouble(x, y, z, 0, new_value_rm)       
    
        self.volumeMapperRm.SetInputData(self.image_data_new_rm)        
    
    def adjustSizeRm(self, dims, checkbox_rm):        
        resizerm = vtk.vtkImageResize()
        resizerm.SetInputData(self.image_data_rm)
        resizerm.SetOutputDimensions(dims[0],dims[1],dims[2])
        resizerm.Update()
        self.image_data_rm = resizerm.GetOutput()
        if checkbox_rm == True:
            self.volumeMapperRm.SetInputData(self.image_data_rm)      
    
    def clearRm(self):        
        self.image_data_rm = self.createEmptyImageData()       
    
    def createEmptyImageData(self):        
        imageData = vtk.vtkImageData()
        imageData.SetDimensions(self.dimensions_vtk_data)  
        
        imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)    
            
        for z in range(self.dimensions_vtk_data[2]):
               for y in range(self.dimensions_vtk_data[1]):
                   for x in range(self.dimensions_vtk_data[0]):                                              
                       imageData.SetScalarComponentFromDouble(x, y, z, 0, 0.0)
        
        return imageData
      
    def setCameraPosition(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(x_pos, y_pos, z_pos)
        
    def setCameraFocalPoint(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetFocalPoint(x_pos, y_pos, z_pos)

    def saveScreenshot(self, string_directory):               
        self.w2if = vtk.vtkWindowToImageFilter()   
        self.w2if.SetInput(self.vtk_widget.GetRenderWindow())
        self.w2if.SetInputBufferTypeToRGBA()
        self.w2if.ReadFrontBufferOff()
        self.w2if.Update()     
        
        self.writer_screenshot = vtk.vtkPNGWriter()               
        self.writer_screenshot.SetInputConnection(self.w2if.GetOutputPort())                
        self.writer_screenshot.SetFileName(string_directory)                   
        self.writer_screenshot.Write()     

   

    
        