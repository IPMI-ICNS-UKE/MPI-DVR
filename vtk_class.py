# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""

import vtk
import numpy as np




class vtk_pipeline:
    def __init__(self):
        # Defintion of visualization parameters 
        self.opacity_max_bolus = 0.5
        self.opacity_max_roadmap = 0.5
        self.threshold_bolus = 0.0
        self.threshold_roadmap = 0.0
        self.intervall_bolus = 1.0
        self.intervall_roadmap = 1.0
        self.min_image_value = 0
        self.max_image_value = 100
        self.dimension_vtk_data = [50, 50, 50]
        self.scale_factor = 1.0          

        # Bolus parameters 
        self.bolusAmbient = 0.4
        self.bolusDiffuse = 0.5
        self.bolusSpecular = 0.05

        # Roadmap parameters        
        self.image_data_roadmap = self.create_empty_image_data()
        self.roadmapAmbient = 0.4
        self.roadmapDiffuse = 0.5 
        self.roadmapSpecular = 0.05        
        self.cutoff_factor_roadmap = 0.05  
        
        # Color map and scalar bar parameters
        self.height_scalarBar = 250        
        self.HSV_color_max_value = 0, 1.0, 1.0
        self.HSV_color_min_value = 0.166, 1.0, 1.0
        
                
        self.lookup_table_matrix = []        
       
         
        # VTK writer to save mha roadmap file
        self.writer = vtk.vtkMetaImageWriter()       
        
        
        
        # Setup of 3D visualization pipeline        
        empty_image_bolus = self.create_empty_image_data()
        empty_image_roadmap = self.create_empty_image_data()   
        self.grid_volume = self.create_grid(empty_image_bolus)
        
        self.volumeMapperBolus = vtk.vtkGPUVolumeRayCastMapper()    
        self.volumeMapperBolus.SetInputData(empty_image_bolus)
        
        self.volumeMapperRoadmap = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeMapperRoadmap.SetInputData(empty_image_roadmap)        
        
        # Placeholder lookup tables are created
        placeholderOpacityTransferFunctionBolus = self.create_lookup_table_slider( 'bolus')        
        placeholderOpacityTransferFunctionRoadmap = self.create_lookup_table_slider( 'roadmap')        
       
        colorTransferFunctionRoadmap = vtk.vtkColorTransferFunction()
        colorTransferFunctionRoadmap.AddRGBPoint(0.0, 0.0, 1.0, 0.0)
        colorTransferFunctionRoadmap.AddRGBPoint(20.0, 0.0, 1.0, 0.0)        
        
        self.volumePropertyBolus = vtk.vtkVolumeProperty()        
        self.volumePropertyBolus.SetScalarOpacity(placeholderOpacityTransferFunctionBolus)
        self.volumePropertyBolus.ShadeOn()
        self.volumePropertyBolus.SetInterpolationTypeToLinear()
        self.volumePropertyBolus.SetAmbient(self.bolusAmbient)
        self.volumePropertyBolus.SetDiffuse(self.bolusDiffuse)
        self.volumePropertyBolus.SetSpecular(self.bolusSpecular)        
        
        self.volumePropertyRoadmap = vtk.vtkVolumeProperty()
        self.volumePropertyRoadmap.SetColor(colorTransferFunctionRoadmap)
        self.volumePropertyRoadmap.SetScalarOpacity(placeholderOpacityTransferFunctionRoadmap)
        self.volumePropertyRoadmap.ShadeOn()
        self.volumePropertyRoadmap.SetInterpolationTypeToLinear()
        self.volumePropertyRoadmap.SetInterpolationTypeToLinear()
        self.volumePropertyRoadmap.SetAmbient(self.roadmapAmbient)
        self.volumePropertyRoadmap.SetDiffuse(self.roadmapDiffuse)
        self.volumePropertyRoadmap.SetSpecular(self.roadmapSpecular)      
        
        self.volumeBolus = vtk.vtkVolume()
        self.volumeBolus.SetMapper(self.volumeMapperBolus)
        self.volumeBolus.SetProperty(self.volumePropertyBolus)      
        
        self.volumeRoadmap = vtk.vtkVolume()
        self.volumeRoadmap.SetMapper(self.volumeMapperRoadmap)
        self.volumeRoadmap.SetProperty(self.volumePropertyRoadmap)   
        
        # Creation of additional actors to be visualized       
        self.scalar_bar_actor = self.create_color_scalar_bar()        
           
        self.text_actor = vtk.vtkTextActor()                
        self.text_actor.GetTextProperty().SetFontSize ( 50)
        self.text_actor.GetTextProperty().SetColor ( 1.0, 0.0, 0.0 )
        self.text_actor.GetTextProperty().SetOpacity ( 0.8)        
        
        # Setup renderer
        self.ren = vtk.vtkRenderer()   
        self.ren.AddVolume(self.volumeRoadmap)
        self.ren.AddVolume(self.volumeBolus)
        self.ren.AddActor2D(self.scalar_bar_actor)
        self.ren.AddActor2D (self.text_actor )        
        self.ren.SetBackground(1.0,1.0,1.0)
        self.ren.ResetCamera()
        

    
    def updateSteepnessBolus(self, intervall_bolus):    
        self.intervall_bolus = intervall_bolus
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table_slider( 'bolus'))    
        self.iren.Initialize()
        self.iren.Start()        
        
    def updateSteepnessRoadmap(self, intervall_roadmap):   
        self.intervall_roadmap = intervall_roadmap
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table_slider('roadmap'))      
        self.iren.Initialize()
        self.iren.Start()    
    
    def updateThresholdBolus(self, threshold_bolus):     
        self.threshold_bolus = threshold_bolus
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table_slider('bolus'))      
        self.iren.Initialize()
        self.iren.Start()
        
    def updateThresholdRoadmap(self, threshold_roadmap):  
        self.threshold_roadmap = threshold_roadmap       
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table_slider('roadmap'))        
        self.iren.Initialize()
        self.iren.Start()          
            
    def updateOpacityRoadmap(self, opacity_max_roadmap):  
        self.opacity_max_roadmap = opacity_max_roadmap
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table_slider('roadmap'))   
        self.iren.Initialize()
        self.iren.Start()    
        
    def updateOpacityBolus(self, opacity_max_bolus):   
        self.opacity_max_bolus = opacity_max_bolus     
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table_slider('bolus'))   
        self.iren.Initialize()
        self.iren.Start()
        
    def updateColorMap(self, threshold):
        colorTransferFunctionBolus = self.create_color_lookup_table()
        self.volumePropertyBolus.SetColor(colorTransferFunctionBolus)
        self.iren.Initialize()
        self.iren.Start()
        
        
    def linearRampFunction(self, variable_ending, x):

        opacity_max_string = 'self.opacity_max_' + variable_ending        
        opacity_max = eval(opacity_max_string)
        
        intervall_string = 'self.intervall_' + variable_ending 
        intervall = eval(intervall_string)
        
        threshold_string = 'self.threshold_' + variable_ending 
        threshold = eval(threshold_string)       

        # Compute function parameters of linear ramp curve (f(x)= m*x + d)        
        m = opacity_max / intervall
        d = -1.0 * threshold * m
        
        return m * x + d         
        
       
        
        
    def create_grid(self, image_data_original):        
        imageDataGrid = vtk.vtkImageData()
        
        x_grid = image_data_original.GetSpacing()[0] * image_data_original.GetDimensions()[0] 
        y_grid = image_data_original.GetSpacing()[1] * image_data_original.GetDimensions()[1] 
        z_grid = image_data_original.GetSpacing()[2] * image_data_original.GetDimensions()[2]         
        
        imageDataGrid.SetDimensions(2,2,2)        
        imageDataGrid.SetSpacing(x_grid, y_grid, z_grid)        
        
        volumeMapperGrid =  vtk.vtkDataSetMapper()  
        volumeMapperGrid.SetInputData(imageDataGrid)
        
        actorGrid = vtk.vtkActor()
        actorGrid.SetMapper(volumeMapperGrid)
        actorGrid.GetProperty().SetRepresentationToWireframe()
        
        return actorGrid         
            

    
        
    def create_lookup_table_slider(self, name):
        """ 
        This function creates a lookup table based on the 
        visualization parameters that can be dynamically changed using 
        the sliders. 
        """
        opacityTransferFunction = vtk.vtkPiecewiseFunction()          
               
        if (name == 'bolus'):        
            x_increment = self.intervall_bolus / 10.0
            x_start = self.threshold_bolus
            x_end = self.threshold_bolus + self.intervall_bolus + x_increment
            x_plateau = self.threshold_bolus + 2.0 *self.intervall_bolus
            
            for x in np.arange(x_start, x_end, x_increment):
                opacityTransferFunction.AddPoint(x, self.linearRampFunction('bolus',x))
            # Add plateau after ramp
            opacityTransferFunction.AddPoint(x_plateau, self.opacity_max_bolus)
            
        
        if (name == 'roadmap'): 
            x_increment = self.intervall_roadmap / 10.0
            x_start = self.threshold_roadmap
            x_end = self.threshold_roadmap + self.intervall_roadmap + x_increment
            x_plateau = self.threshold_roadmap + 2.0 *self.intervall_roadmap
            
            for x in np.arange(x_start, x_end, x_increment):
                opacityTransferFunction.AddPoint(x, self.linearRampFunction('roadmap',x))
            # Add plateau after ramp
            opacityTransferFunction.AddPoint(x_plateau, self.opacity_max_roadmap)
            
        return opacityTransferFunction
    
    
    def create_lookup_table_from_manual_input(self): 
        opacityTransferFunction = vtk.vtkPiecewiseFunction()
        
        for i in range(len([row[0] for row in self.lookup_table_matrix])):
            opacityTransferFunction.AddPoint(self.lookup_table_matrix[i][0], \
                            self.lookup_table_matrix[i][1])
            
        return opacityTransferFunction 
    
    
    def updateVTKparameters(self, min_image_value, max_image_value, dim_images):
        self.total_image_value_range = max_image_value - min_image_value
        
        self.min_image_value = min_image_value
        self.max_image_value = max_image_value
        
        self.threshold_bolus =  self.total_image_value_range / 2.0
        self.threshold_roadmap = self.total_image_value_range / 2.0
        self.intervall_bolus = self.total_image_value_range / 2.0
        self.intervall_roadmap = self.total_image_value_range / 2.0
         
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table_slider('bolus')) 
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table_slider('roadmap')) 
        
        # Update color encoded intensity map             
        self.updateColorMap(self.threshold_bolus)
        self.updateScalarBar()      
        
        # Update dimensions of visualized dataset
        self.dimension_vtk_data = dim_images
        
        # Clear road-map, if new dataset is loaded 
        self.clear_roadmap()
    

    
    
    
    
    def create_color_lookup_table(self):
        colorTransferFunctionBolus = vtk.vtkColorTransferFunction()
        colorTransferFunctionBolus.SetColorSpaceToHSV()
        colorTransferFunctionBolus.AddHSVPoint(self.threshold_bolus, \
            self.HSV_color_min_value[0], self.HSV_color_min_value[1], \
            self.HSV_color_min_value[2])
        colorTransferFunctionBolus.AddHSVPoint(self.max_image_value, \
            self.HSV_color_max_value[0], self.HSV_color_max_value[1], \
            self.HSV_color_max_value[2])        
        
        return colorTransferFunctionBolus
    
    def create_color_scalar_bar(self): 
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange (self.threshold_bolus, self.max_image_value)
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
    
    def updateScalarBar(self): 
        self.ren.RemoveActor2D(self.scalar_bar_actor)
        self.scalar_bar_actor = self.create_color_scalar_bar()
        self.ren.AddActor2D(self.scalar_bar_actor)
        
        
        
      
        
       
    def roadmap_buildup(self, current_image_data):
                         
        self.image_data_new_roadmap = vtk.vtkImageData()        
        self.image_data_new_roadmap.SetDimensions(current_image_data.GetDimensions()[0], \
                 current_image_data.GetDimensions()[1],  \
                 current_image_data.GetDimensions()[2])        
        self.image_data_new_roadmap.AllocateScalars(vtk.VTK_DOUBLE, 1)            
        self.image_data_new_roadmap.SetSpacing(current_image_data.GetSpacing())              
        
        # Compute cutoff value to eliminate background noise contribution to roadmap
        cutoff_roadmap_buildup = self.min_image_value + self.cutoff_factor_roadmap \
                                 * (self.max_image_value -self.min_image_value)
        
            
        for z in range(current_image_data.GetDimensions()[2]):
            for y in range(current_image_data.GetDimensions()[1]):
                for x in range(current_image_data.GetDimensions()[0]):
                    
                    value_roadmap = self.image_data_roadmap.GetScalarComponentAsDouble(x,y,z,0)
                    value_current_image = current_image_data.GetScalarComponentAsDouble(x, y, z, 0)
                    if value_current_image > cutoff_roadmap_buildup: 
                        """ 
                        For the roadmap buildup highest value of 
                        roadmap matrix is compared to highest value 
                        of current image data. 
                        """                                                
                        new_value = max({value_current_image, value_roadmap})   
                        self.image_data_roadmap.SetScalarComponentFromDouble(x,y,z,0,new_value)
                        
                    new_value_roadmap = self.image_data_roadmap.GetScalarComponentAsDouble(x,y,z,0)    
                    self.image_data_new_roadmap.SetScalarComponentFromDouble(x, y, z, 0, new_value_roadmap)       
    
        self.volumeMapperRoadmap.SetInputData(self.image_data_new_roadmap)    
    
    
    def adjust_size_roadmap(self, dims):        
        resizeRoadmap = vtk.vtkImageResize()
        resizeRoadmap.SetInputData(self.image_data_roadmap)
        resizeRoadmap.SetOutputDimensions(dims[0],dims[1],dims[2])
        resizeRoadmap.Update()
        self.image_data_roadmap = resizeRoadmap.GetOutput()
        self.volumeMapperRoadmap.SetInputData(self.image_data_roadmap)  
    
    
    def clear_roadmap(self):        
        self.image_data_roadmap = self.create_empty_image_data()

        
    
    def create_empty_image_data(self):        
        imageData = vtk.vtkImageData()
        imageData.SetDimensions(self.dimension_vtk_data[0], \
                                self.dimension_vtk_data[1], \
                                self.dimension_vtk_data[2])    
        imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)    
            
        for z in range(self.dimension_vtk_data[2]):
               for y in range(self.dimension_vtk_data[1]):
                   for x in range(self.dimension_vtk_data[0]):                                              
                       imageData.SetScalarComponentFromDouble(x, y, z, 0, 0.0)
        
        return imageData
                

      
    def setCameraPosition(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(x_pos, y_pos, z_pos)
        
    def setCameraFocalPoint(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetFocalPoint(x_pos, y_pos, z_pos)

    

   

    
    
        