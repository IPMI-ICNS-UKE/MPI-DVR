# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""

# External libraries
from PyQt5 import QtCore
from PyQt5 import Qt
import datetime
from functools import partial
import os.path

# Own class objects
import mha_reader
import mdf_reader
import manual_input_lookup_table



""" 
This file contains the initUI and the functions directly connected to 
the display widgets (e.g. buttons, sliders, ...) 
"""

def setCameraOperation(self):
    le_input = self.lineedit_camera_control.text()
    i = self.combobox_box_camera.currentIndex()
    
    if i == 0:   # Set camera pos        
        try:  
            coords_str = le_input.split(",")             
            x = float(coords_str[0])
            y = float(coords_str[1])
            z = float(coords_str[2])
            
            print(coords_str)
    
            self.vtk_op.setCameraPosition(x, y, z)    
            self.displayPos()    
            self.iren.Initialize()
            self.iren.Start()
        except:
            print("Type in coordinates in correct form: x,y,z")
        
    if i == 1:   # Set focal point 
        coords_str = le_input.split(",")  
        try:           
            x = float(coords_str[0])
            y = float(coords_str[1])
            z = float(coords_str[2])           
            
            self.vtk_op.setCameraFocalPoint(x, y, z)   
            
            self.displayPos()    
            self.iren.Initialize()
            self.iren.Start()   
        except:
            print("Type in coordinates in correct form: x,y,z")
        
    if i == 2: 
        try: 
            rotation_angle = int(le_input  )
            camera = self.vtk_op.ren.GetActiveCamera()
            camera.Roll(rotation_angle)    
            self.displayPos()    
            self.iren.Initialize()
            self.iren.Start()     
        except:
            print("Type in angle rotation in correct form!")

def placeholderTextCameraLineedit(self, i):
    if i == 0:   # Set camera pos            
        self.lineedit_camera_control.clear()
        self.lineedit_camera_control.setPlaceholderText('x, y, z')           
        
    if i == 1:   # Set focal point  
        self.lineedit_camera_control.clear()           
        self.lineedit_camera_control.setPlaceholderText('x, y, z')           
        
    if i == 2:   # Set angle
        self.lineedit_camera_control.clear()
        self.lineedit_camera_control.setPlaceholderText('angle [°]')  

def setCameraPosition(self):
    x = int( self.camera_position_x.text() )
    y = int( self.camera_position_y.text() )
    z = int( self.camera_position_z.text() )    
    self.vtk_op.setCameraPosition(x, y, z)    
    self.displayPos()    
    self.iren.Initialize()
    self.iren.Start()     
    
def setCameraFocalPoint(self):    
    x = int( self.camera_focal_point_x.text() )
    y = int( self.camera_focal_point_y.text() )
    z = int( self.camera_focal_point_z.text() )    
    self.vtk_op.setCameraFocalPoint(x, y, z)    
    self.displayPos()    
    self.iren.Initialize()
    self.iren.Start()     
    
def rotateCamera(self):     
    rotation_angle = int( self.camera_rotation_angle.text() )
    camera = self.vtk_op.ren.GetActiveCamera()
    
    camera.Roll(rotation_angle)    
    self.displayPos()    
    self.iren.Initialize()
    self.iren.Start()             
    
def interpolateImageData(self, pressed):
    if (pressed == True):  
        try:
            x = int( self.lineedit_interpolation_dim_x.text() )
            y = int( self.lineedit_interpolation_dim_y.text() )
            z = int( self.lineedit_interpolation_dim_z.text() ) 
            
            self.dims = [x, y, z]
            self.interpolation = True
            self.vtk_op.dimension_vtk_data = self.dims
            
            
            self.vtk_op.adjust_size_roadmap(self.dims)
            self.count = self.count - 1
            self.update_status()
            
            #Update image size text display
            image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
            self.label_display_image_data_size.setText(image_size_text)
            
            self.iren.Initialize()
            self.iren.Start()   
        except:
            print("Enter only integer values and fill each field!")
    else: 
        self.dims = self.dims_original
        self.interpolation = False
        self.vtk_op.dimension_vtk_data = self.dims_original
        
        # Resize roadmap matrix    
        self.vtk_op.adjust_size_roadmap(self.dims_original)
        self.count = self.count - 1
        self.update_status()
        
        #Update image size display
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
        self.label_display_image_data_size.setText(image_size_text)
        
        self.iren.Initialize()
        self.iren.Start()          
        
def manualLookupTableBolus(self):  
    if self.manual_lookup_table_bolus == None:
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'bolus', None, 4, 2)
    else: 
        count_rows = len([row[0] for row in self.manual_lookup_table_bolus])
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'bolus', \
                            self.manual_lookup_table_bolus, count_rows, 2)  
        
def manualLookupTableRoadmap(self):  
    if self.manual_lookup_table_roadmap == None:
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'roadmap', None,  4, 2)
    else: 
        count_rows = len([row[0] for row in self.manual_lookup_table_roadmap])
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'roadmap', self.manual_lookup_table_roadmap, count_rows, 2)        

def functionSliderThresholdRoadmap(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 100.0    
    self.threshold_roadmap = self.diagram_op.min_image_value + t  * scale_factor    
    self.diagram_op.threshold_roadmap = self.threshold_roadmap
    self.diagram_op.manual_lookup_table_roadmap = False
    self.diagram_op.drawLookupTable()        
    self.vtk_op.updateThresholdRoadmap(self.threshold_roadmap)     
    
def functionSliderThresholdBolus(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 100.0    
    self.threshold_bolus = self.diagram_op.min_image_value + t  * scale_factor    
    self.diagram_op.threshold_bolus = self.threshold_bolus
    self.diagram_op.manual_lookup_table_bolus = False
    self.diagram_op.drawLookupTable()     
    self.vtk_op.updateThresholdBolus(self.threshold_bolus)
    self.vtk_op.updateColorMap(self.threshold_bolus)
    self.vtk_op.updateScalarBar()    
    
def functionSliderSteepnessRampBolus(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 10000.0
    self.intervall_bolus =  t * scale_factor      
    self.diagram_op.intervall_bolus = self.intervall_bolus
    self.diagram_op.manual_lookup_table_bolus = False
    self.diagram_op.drawLookupTable()        
    self.vtk_op.updateSteepnessBolus(self.intervall_bolus)
    
def functionSliderSteepnessRampRoadmap(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 10000.0
    self.intervall_roadmap =  t * scale_factor    
    self.diagram_op.intervall_roadmap = self.intervall_roadmap
    self.diagram_op.manual_lookup_table_roadmap = False
    self.diagram_op.drawLookupTable()    
    self.vtk_op.updateSteepnessRoadmap(self.intervall_roadmap)

def functionOpacityBolusSlider(self, t):
    self.opacity_max_bolus = t / 100.0    
    self.diagram_op.opacity_max_bolus = self.opacity_max_bolus
    self.diagram_op.manual_lookup_table_bolus = False
    self.diagram_op.drawLookupTable()    
    self.vtk_op.updateOpacityBolus(self.opacity_max_bolus)
    
def functionOpacityRoadmapSlider(self, t):
    self.opacity_max_roadmap = t / 100.0    
    self.diagram_op.opacity_max_roadmap = self.opacity_max_roadmap
    self.diagram_op.manual_lookup_table_roadmap = False
    self.diagram_op.drawLookupTable()    
    self.vtk_op.updateOpacityRoadmap(self.opacity_max_roadmap)    

def checkboxRoadmapSignal(self):      
    """ 
    Function shows / hides the roadmap depending on the status 
    of the corresponding checkbox
    """    
    if not self.checkbox_roadmap_buildup.isChecked():                             
        self.vtk_op.volumeMapperRoadmap.SetInputData(self.vtk_op.create_empty_image_data()) 
        self.iren.Initialize()
        self.iren.Start()
    else:
        self.vtk_op.roadmap_buildup(self.temporary_image)
        self.iren.Initialize()
        self.iren.Start()
        
def checkboxFOVFunction(self):
    """
    Function shows / hides the FOV of the image 
    depending on the status (checked / unchecked) of the corresponding 
    checkbox
    """
    if not self.checkbox_FOV.isChecked():                                      
        self.vtk_op.ren.RemoveActor(self.vtk_op.grid) 
        self.iren.Initialize()
        self.iren.Start()
    else:
        self.vtk_op.grid = self.vtk_op.create_grid(self.temporary_image)
        self.vtk_op.ren.AddActor(self.vtk_op.grid)
        self.iren.Initialize()
        self.iren.Start()
        
def checkboxCameraSpecifications(self):
    """
    Function shows / hides current camera position, focal point and
    rotation
    """
    if not self.checkbox_camera_specifications.isChecked():                                      
        self.vtk_op.ren.RemoveActor(self.vtk_op.textActor) 
        self.iren.Initialize()
        self.iren.Start()
    else:        
        self.vtk_op.ren.AddActor(self.vtk_op.textActor)
        self.iren.Initialize()
        self.iren.Start()

def setPlaybackSpeed1(self, t):
    """ 
    Function gets input t from the QT slider and  
    updates the Qt timer resulting in a modified 
    playback speed. Unit of t_ms is milliseconds.
    """
    self.t_ms = t            
    if not self.source_data_format == 'no_source':
        self.timer.start(self.t_ms)
        if not self.button_start_stop.isChecked(): 
            self.timer.stop()        
    
def loadMHA(self):        
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')        
    name = fname + "/1.mha"     
    if os.path.isfile(name):
        self.source_data_format = 'mha'
        self.directory_source = fname
        self.number_of_total_images =  mha_reader.get_number_of_image_data(self.directory_source)   
        self.dims = mha_reader.return_dims_of_first_image(self.directory_source) 
        self.dims_original = self.dims
        
        # Create histogram and determine min/max image values
        self.diagram_op.computeHistogramDataBin(self.directory_source, 'mha')
        self.diagram_op.drawHistogram()   
        self.diagram_op.drawLookupTable()
        
        # Values are used to update the value range of the slider widgets
        self.threshold_bolus =  self.diagram_op.threshold_bolus
        self.threshold_roadmap =  self.diagram_op.threshold_roadmap
        self.intervall_bolus =  self.diagram_op.intervall_bolus
        self.intervall_roadmap =  self.diagram_op.intervall_roadmap       
          
        # Create internal look up table for VTK pipeline                       
        self.vtk_op.updateVTKparameters(self.diagram_op.min_image_value, 
                self.diagram_op.max_image_value, self.dims)
        
        # Update image count and image size display
        image_count = '1 / '+ str(self.number_of_total_images)      
        self.label_image_count_display.setText(image_count)  
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
        self.label_display_image_data_size.setText(image_size_text)
        
        # Enable all UI buttons, sliders and checkboxes
        self.enableDisableButtons(True) 
        self.update_status()
    else: 
        print("Use valid directory")        

def loadMDF(self):    
    fname = Qt.QFileDialog.getOpenFileName(self, 'c:\\')[0]       
    if fname != '':
        self.source_data_format = 'mdf'
        self.directory_mdf = fname
        
        # Get number of images and image size
        self.number_of_total_images = mdf_reader.get_number_of_images(self.directory_mdf)
        self.dims = mdf_reader.return_dimensions_image_data(self.directory_mdf)  
        self.dims_original = self.dims
        
        # Create histogram and determine min/max image values
        self.diagram_op.computeHistogramDataBin(self.directory_mdf, 'mdf')    
        self.diagram_op.drawHistogram()  
        self.diagram_op.drawLookupTable() 
        
        # Values are used to update the value range of the slider widgets
        self.threshold_bolus =  self.diagram_op.threshold_bolus
        self.threshold_roadmap =  self.diagram_op.threshold_roadmap
        self.intervall_bolus =  self.diagram_op.intervall_bolus
        self.intervall_roadmap =  self.diagram_op.intervall_roadmap     
        
        # Create internal look up table for VTK pipeline                  
        self.vtk_op.updateVTKparameters(self.diagram_op.min_image_value, 
                self.diagram_op.max_image_value, self.dims)
        
        # Update image count and image size display
        image_count = '1 / '+ str(self.number_of_total_images)        
        self.label_image_count_display.setText(image_count)  
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
        self.label_display_image_data_size.setText(image_size_text)
        
        # Enable all UI buttons, sliders and checkboxes
        self.enableDisableButtons(True)     
        self.update_status()
        
def setScreenshotSaveDirectory(self):
    """
    Function opens a simple diaglogue window to select a directory, where 
    subsequently captured screenshots can be saved
    """    
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')        
    self.directory_output = fname     
    self.checkbox_save_images.setChecked(True)
    

def functionCheckboxScalarBar(self):
    """ 
    This function is used to show / hide scalar bar on the visualization 
    screen 
    """
    if not self.checkbox_scalar_bar.isChecked():                             
        self.vtk_op.ren.RemoveActor2D(self.vtk_op.scalar_bar)
        self.iren.Initialize()
        self.iren.Start()
    else:
        self.vtk_op.updateScalarBar()
        self.iren.Initialize()
        self.iren.Start()   
        
def pauseAndPlay(self, pressed):     
    if self.source_data_format == 'no_source':
        print('Please select a source dataset first!')
        self.button_start_stop.setCheckable(True)
        self.button_start_stop.toggle()
        self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))            
    else:    
        if pressed:
            self.timer.start(self.t_ms)
            self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPause))
        else:             
            self.timer.stop()
            self.label_frame_rate_display.setText('-')
            self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))        
    
def showNextImage(self):
    if self.source_data_format == 'no_source':
        print('Please select a source dataset first!')
    else: 
        self.count = self.count + 1        
        if self.count > self.number_of_total_images:
            self.count = 1           
        if self.source_data_format == 'mha':            
            self.temporary_image = \
            mha_reader.create_VTK_data_from_mha_file(self.directory_source, \
                                          self.count, self.interpolation, \
                                          self.dims)          
        if self.source_data_format == 'mdf':            
            self.temporary_image = mdf_reader.create_VTK_data_from_HDF(self.directory_mdf, \
                                     self.count-1, self.interpolation, \
                                     self.dims)        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)         
        if self.checkbox_roadmap_buildup.isChecked(): 
            self.vtk_op.roadmap_buildup(self.temporary_image)    
            
        # Save screenshots of visualized MPI data
        if self.checkbox_save_images.isChecked():
            screenshot_and_save(self)               
        self.iren.Initialize()
        self.iren.Start()    
        
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.label_image_count_display.setText(str(image_count) )
    
def showPreviousImage(self):
    if self.source_data_format == 'no_source':
        print('Please select a source dataset first!')
    else:
        self.count = self.count - 1    
        
        if self.count == 0:        
            self.count = self.number_of_total_images 
            
        if self.source_data_format == 'mha':            
            self.temporary_image = mha_reader.create_VTK_data_from_mha_file(self.directory_source, self.count, self.interpolation, self.dims)
            
        if self.source_data_format == 'mdf':            
            self.temporary_image = mdf_reader.create_VTK_data_from_HDF(self.directory_mdf, self.count-1, self.interpolation, self.dims)        
        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)     
        
        # Save screenshots of visualized MPI data
        if self.checkbox_save_images.isChecked():
            screenshot_and_save(self)     
        
        self.iren.Initialize()
        self.iren.Start()    
    
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.label_image_count_display.setText(str(image_count) )
        
def check_output_directory(self):    
    if self.directory_output != "":
        print(self.directory_output)
        print('Images will be saved to: ', self.directory_output)        
    else:         
        if self.source_data_format == 'mha':
            path_to_source = os.path.normpath(self.directory_source)            
        if self.source_data_format == 'mdf':
            path_to_source = os.path.normpath(self.directory_mdf)            
            path_to_source = os.path.dirname(os.path.realpath(path_to_source))        
        temp_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mydir = os.path.join(path_to_source, temp_time)
        os.makedirs(mydir)        
        self.directory_output = path_to_source + "/" + temp_time
        print('No output adress was given. Images will be saved to: ', self.directory_output)         
        
def screenshot_and_save(self):    
    """ 
    Function saves PNG image of current visualization screen to a defined directory. 
    If no directory is given, a new folder (name composed of current date and time) 
    will be created in the source directory. 
    """
    check_output_directory(self)
    if (os.path.isdir(self.directory_output)):
        name_output = "/%d.png" %self.screenshot_number
        string_directory = self.directory_output + name_output
        self.vtk_op.saveScreenshot(string_directory)
        self.screenshot_number = self.screenshot_number + 1
    
def save_roapmap(self):        
    fileName, _ = Qt.QFileDialog.getSaveFileName(self, \
     "QFileDialog.getSaveFileName()","","Input Files(*.mha)")       
    self.vtk_op.writer_roadmap.SetInputData(self.vtk_op.imageData1)
    self.vtk_op.writer_roadmap.SetFileName(fileName)
    self.vtk_op.writer_roadmap.Write()    
    
    
    
   
def initUI(self):
    """ 
    This function defines the architecture of the GUI and connects 
    the created QT widgets to the corresponding functions defined in this 
    file. The various QT objects are arranged along vertical and horizontal
    axes.
    """ 
    
    self.label_placeholder = Qt.QLabel()
    
    self.button_load_mha_files = Qt.QPushButton('Load .mha files', self)           
    self.button_load_mha_files.clicked.connect(partial(loadMHA, self))  
    
    self.button_load_mdf_file = Qt.QPushButton('Load .mdf file', self)           
    self.button_load_mdf_file.clicked.connect(partial(loadMDF, self))      
        
    self.label_frame_rate = Qt.QLabel(self)
    self.label_frame_rate.setText("Frame rate:  ")
        
    self.label_frame_rate_display = Qt.QLabel(self)
    self.label_frame_rate_display.setText("0.00")
    self.label_frame_rate_display.setStyleSheet("background-color: rgba(255, 255, 255, 100%)")
    
    self.label_image_count = Qt.QLabel(self)
    self.label_image_count.setText("Image #:  ")
    
    self.label_image_count_display = Qt.QLabel(self)
    self.label_image_count_display.setText("- / -")
    self.label_image_count_display.setStyleSheet("background-color: rgba(255, 255, 255, 100%)")
    
    self.button_saving_directory_screenshots = Qt.QPushButton('Choose screenshot directory', self)        
    self.button_saving_directory_screenshots.clicked.connect(partial(setScreenshotSaveDirectory, self))    
    
    self.checkbox_roadmap_buildup = Qt.QCheckBox("Roadmap build-up", self)
    self.checkbox_roadmap_buildup.setChecked(True)
    self.checkbox_roadmap_buildup.stateChanged.connect(partial(checkboxRoadmapSignal, self))
    
    self.checkbox_scalar_bar = Qt.QCheckBox("Show scalar bar", self)
    self.checkbox_scalar_bar.setChecked(True)
    self.checkbox_scalar_bar.stateChanged.connect(partial(functionCheckboxScalarBar, self))
    
    self.checkbox_FOV = Qt.QCheckBox("Show FOV", self)
    self.checkbox_FOV.setChecked(False)
    self.checkbox_FOV.stateChanged.connect(partial(checkboxFOVFunction, self))
    
    self.checkbox_camera_specifications = Qt.QCheckBox("Show camera specifications", self)
    self.checkbox_camera_specifications.setChecked(True)
    self.checkbox_camera_specifications.stateChanged.connect(partial(checkboxCameraSpecifications, self))            
    
    self.button_save_roadmap = Qt.QPushButton('Save roadmap')
    self.button_save_roadmap.clicked.connect( partial(save_roapmap, self) )     
    
    self.checkbox_save_images = Qt.QCheckBox("Save screenshots", self)
    self.checkbox_save_images.setChecked(False)
    self.checkbox_save_images.stateChanged.connect(partial(screenshot_and_save, self)) 

    self.button_start_stop = Qt.QPushButton('', self)
    self.button_start_stop.setCheckable(True)    
    self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))
    self.button_start_stop.clicked[bool].connect(partial(pauseAndPlay, self))
    
    self.button_next_image = Qt.QPushButton('', self)
    self.button_next_image.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaSkipForward))    
    self.button_next_image.clicked.connect(partial(showNextImage, self) )    
    
    self.button_previous_image = Qt.QPushButton('', self)
    self.button_previous_image.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaSkipBackward))    
    self.button_previous_image.clicked.connect(partial(showPreviousImage, self)  )

    self.label_threshold_slider = Qt.QLabel(self)        
    self.label_threshold_slider.setText("Threshold")   
    self.label_threshold_slider.setFixedWidth(125) 
    
    self.slider_steepness_ramp_roadmap = Qt.QSlider(self)
    self.slider_steepness_ramp_roadmap.setMinimum(1)
    self.slider_steepness_ramp_roadmap.setMaximum(10000)
    self.slider_steepness_ramp_roadmap.setProperty("value", 5000)
    self.slider_steepness_ramp_roadmap.setOrientation(QtCore.Qt.Horizontal)
    self.slider_steepness_ramp_roadmap.setObjectName("slider_steepness_ramp_roadmap")
    self.slider_steepness_ramp_roadmap.valueChanged.connect(partial(functionSliderSteepnessRampRoadmap, self))  
    
    self.slider_steepness_ramp_bolus = Qt.QSlider(self)
    self.slider_steepness_ramp_bolus.setMinimum(1)
    self.slider_steepness_ramp_bolus.setMaximum(10000)
    self.slider_steepness_ramp_bolus.setProperty("value", 5000)
    self.slider_steepness_ramp_bolus.setOrientation(QtCore.Qt.Horizontal)
    self.slider_steepness_ramp_bolus.setObjectName("slider_threshold_bolus")
    self.slider_steepness_ramp_bolus.valueChanged.connect(partial(functionSliderSteepnessRampBolus, self) )  
            
    self.slider_threshold_roadmap = Qt.QSlider(self)
    self.slider_threshold_roadmap.setMaximum(100)
    self.slider_threshold_roadmap.setProperty("value", 50)
    self.slider_threshold_roadmap.setOrientation(QtCore.Qt.Horizontal)
    self.slider_threshold_roadmap.setObjectName("slider_threshold_bolus")
    self.slider_threshold_roadmap.valueChanged.connect(partial(functionSliderThresholdRoadmap, self))
    
    self.slider_threshold_bolus = Qt.QSlider(self)
    self.slider_threshold_bolus.setMaximum(100)
    self.slider_threshold_bolus.setProperty("value", 50)
    self.slider_threshold_bolus.setOrientation(QtCore.Qt.Horizontal)
    self.slider_threshold_bolus.setObjectName("slider_threshold_bolus")
    self.slider_threshold_bolus.valueChanged.connect(partial(functionSliderThresholdBolus, self) )        
    
    self.label_opacity_slider = Qt.QLabel(self)        
    self.label_opacity_slider.setText("Opacity");   
    self.label_opacity_slider.setFixedWidth(125) 
    
    self.label_steepness_ramp = Qt.QLabel(self)        
    self.label_steepness_ramp.setText("Steepness ramp");   
    self.label_steepness_ramp.setFixedWidth(125)    
    
    self.slider_opacity_bolus = Qt.QSlider(self)
    self.slider_opacity_bolus.setMaximum(100)
    self.slider_opacity_bolus.setProperty("value", 50)
    self.slider_opacity_bolus.setOrientation(QtCore.Qt.Horizontal)
    self.slider_opacity_bolus.setObjectName("slider_opacity_bolus")     
    self.slider_opacity_bolus.valueChanged.connect(partial(functionOpacityBolusSlider, self))    
    
    self.slider_opacity_roadmap = Qt.QSlider(self)
    self.slider_opacity_roadmap.setMaximum(100)
    self.slider_opacity_roadmap.setProperty("value", 50)
    self.slider_opacity_roadmap.setOrientation(QtCore.Qt.Horizontal)
    self.slider_opacity_roadmap.setObjectName("slider_opacity_roadmap")        
    self.slider_opacity_roadmap.valueChanged.connect(partial(functionOpacityRoadmapSlider, self))       
    
    self.label_playback_speed = Qt.QLabel(self)  
    self.label_playback_speed.setText("Playback Speed") 
    self.label_playback_speed.setFixedWidth(125)        
    
    self.slider_playback_speed = Qt.QSlider(self)
    self.slider_playback_speed.setMaximum(500)
    self.slider_playback_speed.setProperty("value", round(self.t_ms))
    self.slider_playback_speed.setOrientation(QtCore.Qt.Horizontal)
    self.slider_playback_speed.setObjectName("slider_playback_speed")    
    self.slider_playback_speed.setTickInterval(21.5)
    self.slider_playback_speed.setTickPosition(Qt.QSlider.TicksBelow)         
    self.slider_playback_speed.valueChanged.connect(partial(setPlaybackSpeed1, self))  

    self.button_activate_manual_lookup_table_bolus = Qt.QPushButton('', self)
    self.button_activate_manual_lookup_table_bolus.setText("Define lookup table bolus")    
    self.button_activate_manual_lookup_table_bolus.\
        clicked.connect( partial(manualLookupTableBolus, self)  )
        
    self.button_activate_manual_lookup_table_roadmap = Qt.QPushButton('', self)
    self.button_activate_manual_lookup_table_roadmap.setText("Define lookup table roadmap")    
    self.button_activate_manual_lookup_table_roadmap.\
        clicked.connect( partial(manualLookupTableRoadmap, self)  )    
    
    self.label_camera_operations = Qt.QLabel()
    self.label_camera_operations.setText("Manual camera control")
    self.label_camera_operations.setStyleSheet('color: grey')
    self.label_camera_operations.setWordWrap(True)
    self.label_camera_operations.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_manual_defintion_lookup_table = Qt.QLabel()
    self.label_manual_defintion_lookup_table.setText("Manual definition")  
    self.label_manual_defintion_lookup_table.setWordWrap(True)   
    
    self.label_text_above_bolus_slider = Qt.QLabel()
    self.label_text_above_bolus_slider.setText("Bolus")
    self.label_text_above_bolus_slider.setStyleSheet('color: grey')    
    self.label_text_above_bolus_slider.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_roadmap_slider = Qt.QLabel()
    self.label_text_above_roadmap_slider.setText("Roadmap")
    self.label_text_above_roadmap_slider.setStyleSheet('color: grey')    
    self.label_text_above_roadmap_slider.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_image_data = Qt.QLabel()
    self.label_text_above_image_data.setText("Image data")
    self.label_text_above_image_data.setStyleSheet('color: grey')    
    self.label_text_above_image_data.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_playback_settings = Qt.QLabel()
    self.label_text_above_playback_settings.setText("Playback control")
    self.label_text_above_playback_settings.setStyleSheet('color: grey')
    self.label_text_above_playback_settings.setWordWrap(True)
    self.label_text_above_playback_settings.setAlignment(Qt.Qt.AlignCenter)       
    
    self.lineedit_interpolation_dim_x = Qt.QLineEdit(self)
    self.validator_lineedit_interpolation_dim_x = Qt.QIntValidator()
    self.lineedit_interpolation_dim_x.setPlaceholderText('x')
    self.lineedit_interpolation_dim_x.setValidator(self.validator_lineedit_interpolation_dim_x)
    
    self.lineedit_interpolation_dim_y = Qt.QLineEdit(self)
    self.validator_lineedit_interpolation_dim_y = Qt.QIntValidator()
    self.lineedit_interpolation_dim_y.setPlaceholderText('y')
    self.lineedit_interpolation_dim_y.setValidator(self.validator_lineedit_interpolation_dim_y)
    
    self.lineedit_interpolation_dim_z = Qt.QLineEdit(self)
    self.validator_lineedit_interpolation_dim_z = Qt.QIntValidator()
    self.lineedit_interpolation_dim_z.setPlaceholderText('z')
    self.lineedit_interpolation_dim_z.setValidator(self.validator_lineedit_interpolation_dim_z)    
    
    self.label_x_1 = Qt.QLabel()
    self.label_x_1.setText('x')
    self.label_x_1.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_x_2 = Qt.QLabel()
    self.label_x_2.setText('x')
    self.label_x_2.setAlignment(Qt.Qt.AlignCenter)
    
    self.button_set_interpolation_dims = Qt.QPushButton('Dialog', self)
    self.button_set_interpolation_dims.setCheckable(True)          
    self.button_set_interpolation_dims.clicked[bool].connect(partial(interpolateImageData, self))
    self.button_set_interpolation_dims.setText("Activate interpolation")  
    
    self.button_set_camera_operation = Qt.QPushButton('Dialog', self)   
    self.button_set_camera_operation.clicked.connect(partial(setCameraOperation, self))
    self.button_set_camera_operation.setText("SET")   
    
    self.lineedit_camera_control = Qt.QLineEdit(self)
    self.lineedit_camera_control.setPlaceholderText('x, y, z')  
    
    self.label_image_data_size = Qt.QLabel(self)
    self.label_image_data_size.setText("Current image data size:  ")
        
    self.label_display_image_data_size = Qt.QLabel(self)
    self.label_display_image_data_size.setText("-")
    self.label_display_image_data_size.setStyleSheet("background-color: rgba(255, 255, 255, 100%)")
    
    self.combobox_box_camera = Qt.QComboBox()
    self.combobox_box_camera.addItem("Set camera position")
    self.combobox_box_camera.addItem("Set camera focal point")
    self.combobox_box_camera.addItem("Set rotation angle")
    self.combobox_box_camera.currentIndexChanged.connect(partial(placeholderTextCameraLineedit, self))
    

    """
    The following lines define the spatial relation of the defined QT widgets 
    along horizontal and vertical axes (--> Qt.QHBoxLayout / Qt.QVBoxLayout)
    """

    self.hl_load_buttons = Qt.QHBoxLayout()
    self.hl_load_buttons.addWidget(self.button_load_mha_files)
    self.hl_load_buttons.addWidget(self.button_load_mdf_file)    
    self.hl_load_buttons.addWidget(self.button_saving_directory_screenshots)    
    self.hl_load_buttons.addWidget(self.button_save_roadmap)     
    
    self.hl_checkboxes = Qt.QHBoxLayout()
    self.hl_checkboxes.addWidget(self.checkbox_save_images)
    self.hl_checkboxes.addWidget(self.checkbox_FOV)
    self.hl_checkboxes.addWidget(self.checkbox_roadmap_buildup)
    self.hl_checkboxes.addWidget(self.checkbox_scalar_bar)
    self.hl_checkboxes.addWidget(self.checkbox_camera_specifications)    
    
    self.hl_playback_settings = Qt.QHBoxLayout()
    self.hl_playback_settings.addWidget(self.label_image_count)
    self.hl_playback_settings.addWidget(self.label_image_count_display)
    self.hl_playback_settings.addWidget(self.label_frame_rate)
    self.hl_playback_settings.addWidget(self.label_frame_rate_display)    
    self.hl_playback_settings.addWidget(self.label_placeholder)   
    self.hl_playback_settings.addWidget(self.button_previous_image)
    self.hl_playback_settings.addWidget(self.button_start_stop)
    self.hl_playback_settings.addWidget(self.button_next_image)       
    
    self.hl_playback_speed = Qt.QHBoxLayout()
    self.hl_playback_speed.addWidget(self.label_playback_speed)
    self.hl_playback_speed.addWidget(self.slider_playback_speed)     
  
    self.grid_camera_operations = Qt.QGridLayout()    
    self.grid_camera_operations.addWidget(self.combobox_box_camera, 1, 1, 1, 3)
    self.grid_camera_operations.addWidget(self.lineedit_camera_control, 1, 4, 1, 2)
    self.grid_camera_operations.addWidget(self.button_set_camera_operation, 1, 6, 1, 3)       
        
    self.hl_manual_lookup_tables = Qt.QHBoxLayout()
    self.hl_manual_lookup_tables.addWidget(self.button_activate_manual_lookup_table_bolus)
    self.hl_manual_lookup_tables.addWidget(self.button_activate_manual_lookup_table_roadmap)   
        
    self.slider_block = Qt.QGridLayout()    
    self.slider_block.addWidget(self.label_text_above_bolus_slider, 1, 2, 1, 2)
    self.slider_block.addWidget(self.label_text_above_roadmap_slider, 1, 4, 1, 2)    
    self.slider_block.addWidget(self.label_threshold_slider, 4, 1)
    self.slider_block.addWidget(self.slider_threshold_bolus, 4, 2, 2, 2)
    self.slider_block.addWidget(self.slider_threshold_roadmap, 4, 4, 2, 2)       
    self.slider_block.addWidget(self.label_opacity_slider, 6, 1)
    self.slider_block.addWidget(self.slider_opacity_bolus, 6, 2, 2,2)
    self.slider_block.addWidget(self.slider_opacity_roadmap, 6, 4, 2, 2)    
    self.slider_block.addWidget(self.label_steepness_ramp, 8, 1)    
    self.slider_block.addWidget(self.slider_steepness_ramp_bolus, 8, 2, 2, 2)
    self.slider_block.addWidget(self.slider_steepness_ramp_roadmap, 8, 4, 2, 2)     
    self.slider_block.addWidget(self.label_manual_defintion_lookup_table, 10, 1)    
    self.slider_block.addWidget(self.button_activate_manual_lookup_table_bolus, 10, 2, 1, 2)
    self.slider_block.addWidget(self.button_activate_manual_lookup_table_roadmap, 10, 4, 1, 2)    
    
    self.hl_image_specs = Qt.QHBoxLayout()
    self.hl_image_specs.addWidget(self.label_image_data_size)
    self.hl_image_specs.addWidget(self.label_display_image_data_size, stretch=3)
    self.hl_image_specs.addWidget(self.label_placeholder)
    self.hl_image_specs.addWidget(self.button_set_interpolation_dims)    
    self.hl_image_specs.addWidget(self.lineedit_interpolation_dim_x, stretch=1)
    self.hl_image_specs.addWidget(self.label_x_1, stretch=0.5)
    self.hl_image_specs.addWidget(self.lineedit_interpolation_dim_y, stretch=1)
    self.hl_image_specs.addWidget(self.label_x_2, stretch=0.5)
    self.hl_image_specs.addWidget(self.lineedit_interpolation_dim_z, stretch=1)
   
    # Definition of the vertical and horizontal main axis    
    self.vl_main = Qt.QVBoxLayout()    
    self.hl_main = Qt.QHBoxLayout()      
    self.frame.setLayout(self.hl_main)    
    
    # Align all widgets or horizontal layouts along the vertical main axis 
    self.vl_main.addLayout(self.hl_load_buttons)
    self.vl_main.addLayout(self.hl_checkboxes)
    self.vl_main.addWidget(self.diagram_op.canvas)
    self.vl_main.addWidget(self.label_text_above_image_data)    
    self.vl_main.addLayout(self.hl_image_specs)
    self.vl_main.addWidget(self.label_placeholder)    
    self.vl_main.addWidget(self.label_text_above_playback_settings)
    self.vl_main.addLayout(self.hl_playback_settings) 
    self.vl_main.addLayout(self.hl_playback_speed)
    self.vl_main.addWidget(self.label_placeholder)      
    self.vl_main.addLayout(self.slider_block)
    self.vl_main.addWidget(self.label_placeholder)    
    self.vl_main.addWidget(self.label_camera_operations)   
    self.vl_main.addLayout(self.grid_camera_operations) 
    
    # Alignment along horizontal main axis   
    self.hl_main.addLayout(self.vl_main, stretch=1 )
    self.hl_main.addWidget(self.vtkWidget, stretch=2)
    
    
        