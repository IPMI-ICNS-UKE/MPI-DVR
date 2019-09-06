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
        self.threshold_bolus = 20.0
        self.threshold_roadmap = 20.0
        self.intervall_bolus = 100.0
        self.intervall_roadmap = 100.0
        self.min_image_value = 0
        self.max_image_value = 100
        self.dimension_vtk_data = [50, 50, 50]
        self.scale_factor = 1.0    
        self.imageData1 = self.create_empty_image_data()
        self.x = np.zeros((self.dimension_vtk_data[0], \
                   self.dimension_vtk_data[1], \
                   self.dimension_vtk_data[2]))
        self.cutoff_factor_roadmap = 0.05
        self.angio_lower_range  = 12000
        self.angio_upper_range = 55000
        
        self.height_scalarBar = 250
        
        self.HSV_color_max_value = 0, 1.0, 1.0
        self.HSV_color_min_value = 0.166, 1.0, 1.0
        
        self.lookup_table_matrix = []
        
       
        
        
        self.dict={
                'bolus' : [self.opacity_max_bolus, self.threshold_bolus, self.intervall_bolus],
                'roadmap' : [self.opacity_max_roadmap, self.threshold_roadmap, self.intervall_roadmap]
                }
         
        # VTK writer for creation of mha roadmap file
        self.writer = vtk.vtkMetaImageWriter()
        
        
        
        
        
        # Setup of 3D visualization pipeline        
        image_placeholder = self.create_empty_image_data()
        image_placeholder2 = self.create_empty_image_data()   
        self.grid_volume = self.create_grid(image_placeholder)
        
        self.volumeMapperBolus = vtk.vtkGPUVolumeRayCastMapper()    
        self.volumeMapperBolus.SetInputData(image_placeholder)
        
        self.volumeMapperRoadmap = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeMapperRoadmap.SetInputData(image_placeholder2)        
        
        opacityTransferFunctionBolus = self.create_lookup_table( 'bolus')        
        opacityTransferFunctionRoadmap = self.create_lookup_table( 'roadmap')        
       
# =============================================================================
#         # Create transfer mapping scalar value to color
#         colorTransferFunctionBolus = vtk.vtkColorTransferFunction()
#         colorTransferFunctionBolus.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
#         colorTransferFunctionBolus.AddRGBPoint(20.0, 1.0, 0.0, 0.0)
#         
# =============================================================================
        

        
        colorTransferFunctionRoadmap = vtk.vtkColorTransferFunction()
        colorTransferFunctionRoadmap.AddRGBPoint(0.0, 0.0, 1.0, 0.0)
        colorTransferFunctionRoadmap.AddRGBPoint(20.0, 0.0, 1.0, 0.0)
        
        
        self.volumePropertyBolus = vtk.vtkVolumeProperty()
        #self.volumePropertyBolus.SetColor(colorTransferFunctionBolus)
        self.volumePropertyBolus.SetScalarOpacity(opacityTransferFunctionBolus)
        self.volumePropertyBolus.ShadeOn()
        self.volumePropertyBolus.SetInterpolationTypeToLinear()
        self.volumePropertyBolus.SetAmbient(0.4)
        self.volumePropertyBolus.SetDiffuse(0.5)
        self.volumePropertyBolus.SetSpecular(0.05)
        
        
        self.volumePropertyRoadmap = vtk.vtkVolumeProperty()
        self.volumePropertyRoadmap.SetColor(colorTransferFunctionRoadmap)
        self.volumePropertyRoadmap.SetScalarOpacity(opacityTransferFunctionRoadmap)
        self.volumePropertyRoadmap.ShadeOn()
        self.volumePropertyRoadmap.SetInterpolationTypeToLinear()
        
        self.volumeBolus = vtk.vtkVolume()
        self.volumeBolus.SetMapper(self.volumeMapperBolus)
        self.volumeBolus.SetProperty(self.volumePropertyBolus)      
        
        self.volumeRoadmap = vtk.vtkVolume()
        self.volumeRoadmap.SetMapper(self.volumeMapperRoadmap)
        self.volumeRoadmap.SetProperty(self.volumePropertyRoadmap)   
        
        self.scalar_bar = self.create_color_scalar_bar()
        
        

    
        self.textActor = vtk.vtkTextActor()        
        self.textActor.SetPosition ( 200   , 200 )
        self.textActor.GetTextProperty().SetFontSize ( 50)
        self.textActor.GetTextProperty().SetColor ( 1.0, 0.0, 0.0 )
        self.textActor.GetTextProperty().SetOpacity ( 0.8)
        

        
        
        
        self.ren = vtk.vtkRenderer()

    
        self.ren.AddVolume(self.volumeRoadmap)
        self.ren.AddVolume(self.volumeBolus)
        self.ren.AddActor2D(self.scalar_bar)
        self.ren.AddActor2D (self.textActor )
        #self.ren.AddActor2D ( textActor2 )
        
        self.ren.SetBackground(1.0,1.0,1.0)
        self.ren.ResetCamera()
        

    
    def updateSteepnessBolus(self, intervall_bolus):    
        self.intervall_bolus = intervall_bolus
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table( 'bolus'))    
        self.iren.Initialize()
        self.iren.Start()        
        
    def updateSteepnessRoadmap(self, intervall_roadmap):   
        self.intervall_roadmap = intervall_roadmap
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table('roadmap'))      
        self.iren.Initialize()
        self.iren.Start()    
    
    def updateThresholdBolus(self, threshold_bolus):     
        self.threshold_bolus = threshold_bolus
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table('bolus'))      
        self.iren.Initialize()
        self.iren.Start()
        
    def updateThresholdRoadmap(self, threshold_roadmap):  
        self.threshold_roadmap = threshold_roadmap       
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table('roadmap'))        
        self.iren.Initialize()
        self.iren.Start()          
            
    def updateOpacityRoadmap(self, opacity_max_roadmap):  
        self.opacity_max_roadmap = opacity_max_roadmap
        self.volumePropertyRoadmap.SetScalarOpacity(self.create_lookup_table('roadmap'))   
        self.iren.Initialize()
        self.iren.Start()    
        
    def updateOpacityBolus(self, opacity_max_bolus):   
        self.opacity_max_bolus = opacity_max_bolus     
        self.volumePropertyBolus.SetScalarOpacity(self.create_lookup_table('bolus'))   
        self.iren.Initialize()
        self.iren.Start()
        
    def updateColorMap(self, threshold):
        colorTransferFunctionBolus = self.create_color_lookup_table()
        self.volumePropertyBolus.SetColor(colorTransferFunctionBolus)
        self.iren.Initialize()
        self.iren.Start()
        
    def create_grid(self, image_data_original):
        """
        		vtkSmartPointer<vtkImageData> imageDataGrid =  vtkSmartPointer<vtkImageData>::New();
		imageDataGrid->SetDimensions(2,2,2);
		imageDataGrid->SetSpacing(x_grid, y_grid, z_grid);
		imageDataGrid->SetOrigin(0.0, 0.0, 0.0);
        """
        
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
        


        
    def create2Dprojection(self, directory_source_angio):
        self.directory_source_angio = directory_source_angio
        
        # create reader
        self.imageReaderAngio = vtk.vtkMetaImageReader() 
        self.imageReaderAngio.SetFileName(self.directory_source_angio) 
        self.imageReaderAngio.Update()     
        
        # create vtk image
        self.imageDataTemp = self.imageReaderAngio.GetOutput()
        
# =============================================================================
#         resize = vtk.vtkImageResize()
#         resize.SetInputData(self.imageDataTemp)
#         resize.SetOutputDimensions(200, 200, 200)
#         resize.Update()
#         self.imageDataTemp = resize.GetOutput()
# =============================================================================
        
        
# =============================================================================
#         for z in range(100):
#             for y in range(100):
#                 for x in range(100):
#                     a = self.imageDataTemp.GetScalarComponentAsDouble(x, y, z, 0 )  
#                     if a < 28000: 
#                         self.imageDataTemp.SetScalarComponentFromDouble(x, y, z, 0, a / 2.0 )  
# =============================================================================
               
                         
        
        # create image reslice mapper
        self.ResliceMapperAngio = vtk.vtkImageResliceMapper()
        self.ResliceMapperAngio.SetInputData(self.imageDataTemp)
        
        
        
        self.ResliceMapperAngio.SetSlabThickness(1000)
        self.ResliceMapperAngio.SliceFacesCameraOn()
        self.ResliceMapperAngio.SliceAtFocalPointOn()
        self.ResliceMapperAngio.BorderOff()
        self.ResliceMapperAngio.SetSlabTypeToMax()
       
        self.ImageSliceAngio = vtk.vtkImageSlice()
    	
        self.ImagePropertyAngio = vtk.vtkImageProperty()
    	
        self.ImageSliceAngio.SetMapper(self.ResliceMapperAngio)
        self.ImageSliceAngio.GetProperty().SetInterpolationTypeToNearest()
        self.ImageSliceAngio.GetProperty().SetColorWindow(100000)
        
       
        
        self.TableAngio = vtk.vtkLookupTable()
        self.TableAngio.SetTableRange(self.angio_lower_range,self.angio_upper_range)
        self.TableAngio.SetValueRange(1.0,0.0)
        self.TableAngio.SetSaturationRange (0.0, 0.0)
        self.TableAngio.SetAlphaRange(0.1, 1.0)
        self.TableAngio.SetHueRange (0.0, 0.0)
        self.TableAngio.UseBelowRangeColorOn ()
        
        self.TableAngio.SetBelowRangeColor (0.9, 0.9, 0.9, 0.1)
        self.TableAngio.SetAboveRangeColor (0, 0, 0, 1.0)
        self.TableAngio.UseAboveRangeColorOff ()
        self.TableAngio.SetNumberOfTableValues (1000)
# =============================================================================
#         self.TableAngio.SetTableValue(0     , 0.1     , 0.1     , 0.1, 0.1)
#         self.TableAngio.SetTableValue(1     , 0.1    , 0.1     , 0.1, 0.8)
# =============================================================================
        
        self.TableAngio.SetRampToSCurve () 
        #self.TableAngio.SetRampToSQRT ()
        #self.TableAngio.SetRampToLinear ()
        self.TableAngio.Build()
        
        
        """
    table_angio->SetTableRange(12000,55000);
    table_angio->SetValueRange(1.0,0.0);
    table_angio->SetSaturationRange (0.0, 0.0);
    table_angio->SetHueRange (0, 0);
    //table_angio->UseBelowRangeColorOn ();
    //table_angio->UseAboveRangeColorOn ();
    //table_angio->SetBelowRangeColor (0, 0, 0, 0.0);
    //table_angio->SetAboveRangeColor (0, 0, 0, 0.0);
    table_angio->SetNumberOfTableValues (500);
    table_angio->SetRampToSCurve();
   // table_angio->SetTableValue(0     , 1     , 1     , 1, 0.2);
   // table_angio->SetTableValue(1.0     , 0     , 0    , 0, 0.4);
    table_angio->SetScaleToLinear ();
	imageSliceAngio->GetProperty()->UseLookupTableScalarRangeOn();
	imageSliceAngio->GetProperty()->SetLookupTable(table_angio);
        """
        
        
        #self.TableAngio.SetRampToSCurve()
    
      
        self.ImageSliceAngio.GetProperty().UseLookupTableScalarRangeOn()
        #self.ImageSliceAngio.GetProperty().UseLookupTableScalarRangeOff()
        self.ImageSliceAngio.GetProperty().SetLookupTable(self.TableAngio)
        self.ImageSliceAngio.GetProperty().SetOpacity(1.0)
       
        
        
        self.renAngio = vtk.vtkRenderer()
        
        self.renAngio.SetBackground(0.9,0.9,0.9)
        self.renAngio.AddActor(self.ImageSliceAngio)    
    
    
        
# =============================================================================
#         
#         
#         self.RenderWindow = vtk.vtkRenderWindow()
#         self.RenderWindow.AddRenderer(self.renAngio)
#         self.RenderWindowInteractor = vtk.vtkRenderWindowInteractor()
#         self.RenderWindowInteractor.SetRenderWindow(self.RenderWindow)    
#         self.RenderWindow.Render()
#         self.RenderWindowInteractor.Start() 
#     
# =============================================================================
            

    def create_and_update_lookup_table_angio(self):
        
        self.TableAngio.SetTableRange(self.angio_lower_range,self.angio_upper_range)
        self.TableAngio.Build()        
        self.ImageSliceAngio.GetProperty().SetLookupTable(self.TableAngio)
        
        
            
    def linearRampFunction(self, variable_ending, x):
        # Frage an Rene: 
        # Auf die Parameter von Bolus / Roadmap eher wie hier über eval() zugreifen 
        # oder eher wie in "create_lookup_table", also per if-Abfrage beides explizit definieren????
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
    
        
    def create_lookup_table(self, name):
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
    
    def create_color_lookup_table(self):
        colorTransferFunctionBolus = vtk.vtkColorTransferFunction()
        colorTransferFunctionBolus.SetColorSpaceToHSV()
        colorTransferFunctionBolus.AddHSVPoint(self.threshold_bolus, \
            self.HSV_color_min_value[0], self.HSV_color_min_value[1], \
            self.HSV_color_min_value[2])
        colorTransferFunctionBolus.AddHSVPoint(self.max_image_value, \
            self.HSV_color_max_value[0], self.HSV_color_max_value[1], \
            self.HSV_color_max_value[2])
        #self.volumePropertyBolus.SetColor(colorTransferFunctionBolus)
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

            
    def roadmap_buildup(self, temporary_image):
                         
        self.imageData1 = vtk.vtkImageData()
        
        self.imageData1.SetDimensions(temporary_image.GetDimensions()[0], \
                 temporary_image.GetDimensions()[1],  \
                 temporary_image.GetDimensions()[2])
        
        self.imageData1.AllocateScalars(vtk.VTK_DOUBLE, 1)    
        
        self.imageData1.SetSpacing(temporary_image.GetSpacing())
                  
        imageDataTemp = temporary_image    
        
        # Compute cutoff value to eliminate background noise
        cutoff_roadmap_buildup = self.min_image_value + self.cutoff_factor_roadmap * (self.max_image_value -self.min_image_value)
        
            
        for z in range(temporary_image.GetDimensions()[2]):
            for y in range(temporary_image.GetDimensions()[1]):
                for x in range(temporary_image.GetDimensions()[0]):
                    
                    
                    k = imageDataTemp.GetScalarComponentAsDouble(x, y, z, 0)
                    if k > cutoff_roadmap_buildup: 
                        """ 
                        FOr the roadmap buildup highest value of 
                        roadmap matrix is compared to highest value 
                        of current image data. 
                        """
                        self.x[x,y,z]= max({self.x[x,y,z], k})                    
                        
                    self.imageData1.SetScalarComponentFromDouble(x, y, z, 0, self.x[x,y,z])         
        
    
        self.volumeMapperRoadmap.SetInputData(self.imageData1)    
    
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
                
    def updateScalarBar(self): 
        self.ren.RemoveActor2D(self.scalar_bar)
        self.scalar_bar = self.create_color_scalar_bar()
        self.ren.AddActor2D(self.scalar_bar)
      
    def setCameraPosition(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(x_pos, y_pos, z_pos)
        
    def setCameraFocalPoint(self, x_pos, y_pos, z_pos):
        camera = self.ren.GetActiveCamera()
        camera.SetFocalPoint(x_pos, y_pos, z_pos)
        
        
    def vtk_pipeline_setup(self):
        
        
        image_placeholder = create_empty_image_data(self)
        image_placeholder2 = create_empty_image_data(self)
        
        self.volumeMapperBolus = vtk.vtkGPUVolumeRayCastMapper()    
        self.volumeMapperBolus.SetInputData(image_placeholder)
        
        self.volumeMapperRoadmap = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeMapperRoadmap.SetInputData(image_placeholder2)        
     
        
        opacityTransferFunctionBolus = create_lookup_table(self, 'bolus')
        
        opacityTransferFunctionRoadmap = create_lookup_table(self, 'roadmap')
        
       
        # Create transfer mapping scalar value to color
        colorTransferFunctionBolus = vtk.vtkColorTransferFunction()
        colorTransferFunctionBolus.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
        colorTransferFunctionBolus.AddRGBPoint(20.0, 1.0, 0.0, 0.0)
        
        colorTransferFunctionRoadmap = vtk.vtkColorTransferFunction()
        colorTransferFunctionRoadmap.AddRGBPoint(0.0, 0.0, 1.0, 0.0)
        colorTransferFunctionRoadmap.AddRGBPoint(20.0, 0.0, 1.0, 0.0)
        
        # The property describes how the data will look
        self.volumePropertyBolus = vtk.vtkVolumeProperty()
        self.volumePropertyBolus.SetColor(colorTransferFunctionBolus)
        self.volumePropertyBolus.SetScalarOpacity(opacityTransferFunctionBolus)
        self.volumePropertyBolus.ShadeOn()
        self.volumePropertyBolus.SetInterpolationTypeToLinear()
        
        self.volumePropertyRoadmap = vtk.vtkVolumeProperty()
        self.volumePropertyRoadmap.SetColor(colorTransferFunctionRoadmap)
        self.volumePropertyRoadmap.SetScalarOpacity(opacityTransferFunctionRoadmap)
        self.volumePropertyRoadmap.ShadeOn()
        self.volumePropertyRoadmap.SetInterpolationTypeToLinear()
        
        self.volumeBolus = vtk.vtkVolume()
        self.volumeBolus.SetMapper(self.volumeMapperBolus)
        self.volumeBolus.SetProperty(self.volumePropertyBolus)      
        
        self.volumeRoadmap = vtk.vtkVolume()
        self.volumeRoadmap.SetMapper(self.volumeMapperRoadmap)
        self.volumeRoadmap.SetProperty(self.volumePropertyRoadmap)   
        
        self.ren = vtk.vtkRenderer()
    
        self.ren.AddVolume(self.volumeRoadmap)
        self.ren.AddVolume(self.volumeBolus)
        
        self.ren.SetBackground(.6,.6,.6)
        self.ren.ResetCamera()
    

   

    
    
        