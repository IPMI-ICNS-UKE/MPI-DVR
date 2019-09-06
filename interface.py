# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""

import vtk
from PyQt5 import QtCore
from PyQt5 import Qt

import datetime

from functools import partial



import mha_reader
import mdf_reader

import manual_input_lookup_table

import os.path

""" 
This file contains the initUI and the functions directly connected to 
the display widgets (e.g. buttons, sliders, ...) 
"""

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
        
def manualLookupTableBolus(self):  
    if self.manual_lookup_table_bolus == None:
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'bolus', 4, 2)
    else: 
        count_rows = len([row[0] for row in self.manual_lookup_table_bolus])
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'bolus', count_rows, 2)        
        self.subwindow_lookup_table.lookup_table_matrix = self.manual_lookup_table_bolus
        self.subwindow_lookup_table.buildupLookupTableFromLookmatrix()        

def manualLookupTableRoadmap(self):  
    if self.manual_lookup_table_roadmap == None:
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'roadmap',  4, 2)
    else: 
        count_rows = len([row[0] for row in self.manual_lookup_table_roadmap])
        self.subwindow_lookup_table = manual_input_lookup_table.TableView(self, 'roadmap', count_rows, 2)        
        self.subwindow_lookup_table.lookup_table_matrix = self.manual_lookup_table_roadmap
        self.subwindow_lookup_table.buildupLookupTableFromLookmatrix()   

def functionThresholdRoadmapSlider(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 100.0    
    self.threshold_roadmap = self.diagram_op.min_image_value + t  * scale_factor    
    self.diagram_op.threshold_roadmap = self.threshold_roadmap
    self.diagram_op.manual_lookup_table_roadmap = False
    self.diagram_op.drawLookupTable()        
    self.vtk_op.updateThresholdRoadmap(self.threshold_roadmap)     
    
def functionThresholdBolusSlider(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 100.0    
    self.threshold_bolus = self.diagram_op.min_image_value + t  * scale_factor    
    self.diagram_op.threshold_bolus = self.threshold_bolus
    self.diagram_op.manual_lookup_table_bolus = False
    self.diagram_op.drawLookupTable()     
    self.vtk_op.updateThresholdBolus(self.threshold_bolus)
    self.vtk_op.updateColorMap(self.threshold_bolus)
    self.vtk_op.updateScalarBar()    
    
def functionSteepnessBolusSlider(self, t):
    scale_factor = ( self.diagram_op.max_image_value - self.diagram_op.min_image_value ) / 10000.0
    self.intervall_bolus =  t * scale_factor      
    self.diagram_op.intervall_bolus = self.intervall_bolus
    self.diagram_op.manual_lookup_table_bolus = False
    self.diagram_op.drawLookupTable()        
    self.vtk_op.updateSteepnessBolus(self.intervall_bolus)
    
def functionSteepnessRoadmapSlider(self, t):
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

def checkbox_roadmap_signal(self):      
    """ 
    Function shows / hides the roadmap depending on the status 
    of the corresponding checkbox
    """    
    if not self.roadmap_buildup_checkbox.isChecked():                             
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
    if not self.format == 'no_source':
        self.timer.start(self.t_ms)
        if not self.start_stop_button.isChecked(): 
            self.timer.stop()        
    
def setMHASourceDirectory(self):        
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')        
    name = fname + "/1.mha"     
    if os.path.isfile(name):
        self.format = 'mha'
        self.directory_source = fname
        self.number_of_total_images =  mha_reader.get_number_of_image_data(self.directory_source)   
        self.dims = mha_reader.return_dims_of_first_image(self.directory_source) 
        
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
        self.vtk_op.initLookupTableSliders(self.diagram_op.min_image_value, 
                self.diagram_op.max_image_value, self.dims)
        
        # Update image count display
        image_count = '1 / '+ str(self.number_of_total_images)      
        self.image_count_display.setText(image_count)  
        
        # Enable all UI buttons, sliders and checkboxes
        self.enable_disable_buttons(True) 
        self.update_status()
    else: 
        print("Use valid directory")    
    

def setMDFSourceDirectory(self):    
    fname = Qt.QFileDialog.getOpenFileName(self, 'c:\\')[0]       
    if fname != '':
        self.format = 'mdf'
        self.directory_mdf = fname
        
        # Get number of images and image size
        self.number_of_total_images = mdf_reader.get_number_of_images(self.directory_mdf)
        self.dims = mdf_reader.return_dimensions_image_data(self.directory_mdf)  
        
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
        self.vtk_op.initLookupTableSliders(self.diagram_op.min_image_value, 
                self.diagram_op.max_image_value, self.dims)
        
        # Update image count display
        image_count = '1 / '+ str(self.number_of_total_images)        
        self.image_count_display.setText(image_count)  
        
        # Enable all UI buttons, sliders and checkboxes
        self.enable_disable_buttons(True)     
        self.update_status()
        
def setScreenshotSaveDirectory(self):
    """
    Function opens a simple diaglogue window to select a directory, where 
    subsequently captured screenshots can be saved
    """    
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')        
    self.directory_output = fname     
    self.save_images_checkbox.setChecked(True)
    

def function_checkbox_scalar_bar(self):
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
        
def pause_and_play(self, pressed):     
    if self.format == 'no_source':
        print('Please select a source dataset first!')
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.toggle()
        self.start_stop_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))            
    else:    
        if pressed:
            self.timer.start(self.t_ms)
            self.start_stop_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPause))
        else:             
            self.timer.stop()
            self.frame_rate_display.setText('-')
            self.start_stop_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))        
    
def show_next_image(self):
    if self.format == 'no_source':
        print('Please select a source dataset first!')
    else: 
        self.count = self.count + 1        
        if self.count > self.number_of_total_images:
            self.count = 1           
        if self.format == 'mha':            
            self.temporary_image = \
            mha_reader.create_VTK_data_from_mha_file(self.directory_source, \
                                          self.count, self.interpolation, \
                                          self.dims)          
        if self.format == 'mdf':            
            self.temporary_image = mdf_reader.create_VTK_data_from_HDF(self.directory_mdf, \
                                     self.count-1, self.interpolation, \
                                     self.dims)        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)         
        if self.roadmap_buildup_checkbox.isChecked(): 
            self.vtk_op.roadmap_buildup(self.temporary_image)    
            
        # Save screenshots of visualized MPI data
        if self.save_images_checkbox.isChecked():
            screenshot_and_save(self)               
        self.iren.Initialize()
        self.iren.Start()    
        
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.image_count_display.setText(str(image_count) )
    
def show_previous_image(self):
    if self.format == 'no_source':
        print('Please select a source dataset first!')
    else:
        self.count = self.count - 1    
        
        if self.count == 0:        
            self.count = self.number_of_total_images 
            
        if self.format == 'mha':            
            self.temporary_image = mha_reader.create_VTK_data_from_mha_file(self.directory_source, self.count, self.interpolation, self.dims)
            
        if self.format == 'mdf':            
            self.temporary_image = mdf_reader.create_VTK_data_from_HDF(self.directory_mdf, self.count-1, self.interpolation, self.dims)        
        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)     
        
        # Save screenshots of visualized MPI data
        if self.save_images_checkbox.isChecked():
            screenshot_and_save(self)     
        
        self.iren.Initialize()
        self.iren.Start()    
    
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.image_count_display.setText(str(image_count) )
        
def check_output_directory(self):    
    if self.directory_output != "":
        print(self.directory_output)
        print('Images will be saved to: ', self.directory_output)        
    else:         
        if self.format == 'mha':
            path_to_source = os.path.normpath(self.directory_source)            
        if self.format == 'mdf':
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
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.vtkWidget.GetRenderWindow())
        w2if.Update()
        writer = vtk.vtkPNGWriter()
        name_output = "/%d.png" %self.screenshot_number          
        writer.SetFileName(self.directory_output + name_output)        
        writer.SetInputConnection(w2if.GetOutputPort())            
        self.screenshot_number = self.screenshot_number + 1
        writer.Write()     
    
def save_roapmap(self):        
    fileName, _ = Qt.QFileDialog.getSaveFileName(self, \
     "QFileDialog.getSaveFileName()","","Input Files(*.mha)")       
    self.vtk_op.writer.SetInputData(self.vtk_op.imageData1)
    self.vtk_op.writer.SetFileName(fileName)
    self.vtk_op.writer.Write()    
    
    
    
   
def initUI(self):
    """ 
    This function defines the architecture of the GUI and connects 
    the created QT widgets to the corresponding functions defined in this 
    file. The various QT objects are arranged along vertical and horizontal
    axes.
    """ 
    
    self.placeholder = Qt.QLabel()
    
    self.button_load_mha_files = Qt.QPushButton('Load .mha files', self)           
    self.button_load_mha_files.clicked.connect(partial(setMHASourceDirectory, self))  
    
    self.button_load_mdf_file = Qt.QPushButton('Load .mdf file', self)           
    self.button_load_mdf_file.clicked.connect(partial(setMDFSourceDirectory, self))      
        
    self.frame_rate_label = Qt.QLabel(self)
    self.frame_rate_label.setText("Frame rate:  ")
        
    self.frame_rate_display = Qt.QLabel(self)
    self.frame_rate_display.setText("0.00")
    self.frame_rate_display.setStyleSheet("background-color: rgba(255, 255, 255, 100%)")
    
    self.image_count_label = Qt.QLabel(self)
    self.image_count_label.setText("Image #:  ")
    
    self.image_count_display = Qt.QLabel(self)
    self.image_count_display.setText("- / -")
    self.image_count_display.setStyleSheet("background-color: rgba(255, 255, 255, 100%)")
    
    self.button_saving_directory_screenshots = Qt.QPushButton('Choose screenshot directory', self)        
    self.button_saving_directory_screenshots.clicked.connect(partial(setScreenshotSaveDirectory, self))    
    
    self.roadmap_buildup_checkbox = Qt.QCheckBox("Roadmap build-up", self)
    self.roadmap_buildup_checkbox.setChecked(True)
    self.roadmap_buildup_checkbox.stateChanged.connect(partial(checkbox_roadmap_signal, self))
    
    self.checkbox_scalar_bar = Qt.QCheckBox("Show scalar bar", self)
    self.checkbox_scalar_bar.setChecked(True)
    self.checkbox_scalar_bar.stateChanged.connect(partial(function_checkbox_scalar_bar, self))
    
    self.checkbox_FOV = Qt.QCheckBox("Show FOV", self)
    self.checkbox_FOV.setChecked(False)
    self.checkbox_FOV.stateChanged.connect(partial(checkboxFOVFunction, self))
    
    self.checkbox_camera_specifications = Qt.QCheckBox("Show camera specifications", self)
    self.checkbox_camera_specifications.setChecked(True)
    self.checkbox_camera_specifications.stateChanged.connect(partial(checkboxCameraSpecifications, self))            
    
    self.button_save_roadmap = Qt.QPushButton('Save roadmap')
    self.button_save_roadmap.clicked.connect( partial(save_roapmap, self) )     
    
    self.save_images_checkbox = Qt.QCheckBox("Save screenshots", self)
    self.save_images_checkbox.setChecked(False)
    self.save_images_checkbox.stateChanged.connect(partial(screenshot_and_save, self)) 

    self.start_stop_button = Qt.QPushButton('', self)
    self.start_stop_button.setCheckable(True)    
    self.start_stop_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))
    self.start_stop_button.clicked[bool].connect(partial(pause_and_play, self))
    
    self.next_image_button = Qt.QPushButton('', self)
    self.next_image_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaSkipForward))    
    self.next_image_button.clicked.connect(partial(show_next_image, self) )    
    
    self.previous_image_button = Qt.QPushButton('', self)
    self.previous_image_button.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaSkipBackward))    
    self.previous_image_button.clicked.connect(partial(show_previous_image, self)  )

    self.label_bolus_slider = Qt.QLabel(self)        
    self.label_bolus_slider.setText("Threshold Bolus")   
    self.label_bolus_slider.setFixedWidth(125) 
    
    self.label_roadmap_slider = Qt.QLabel(self)        
    self.label_roadmap_slider.setText("Threshold Roadmap")  
    self.label_roadmap_slider.setFixedWidth(125) 
    
    self.steepnessRoadmapSlider = Qt.QSlider(self)
    self.steepnessRoadmapSlider.setMinimum(1)
    self.steepnessRoadmapSlider.setMaximum(10000)
    self.steepnessRoadmapSlider.setProperty("value", 5000)
    self.steepnessRoadmapSlider.setOrientation(QtCore.Qt.Horizontal)
    self.steepnessRoadmapSlider.setObjectName("SteepnessRoadmapSlider")
    self.steepnessRoadmapSlider.valueChanged.connect(partial(functionSteepnessRoadmapSlider, self))  
    
    self.steepnessBolusSlider = Qt.QSlider(self)
    self.steepnessBolusSlider.setMinimum(1)
    self.steepnessBolusSlider.setMaximum(10000)
    self.steepnessBolusSlider.setProperty("value", 5000)
    self.steepnessBolusSlider.setOrientation(QtCore.Qt.Horizontal)
    self.steepnessBolusSlider.setObjectName("ThresholdBolusSlider")
    self.steepnessBolusSlider.valueChanged.connect(partial(functionSteepnessBolusSlider, self) )  
            
    self.thresholdRoadmapSlider = Qt.QSlider(self)
    self.thresholdRoadmapSlider.setMaximum(100)
    self.thresholdRoadmapSlider.setProperty("value", 50)
    self.thresholdRoadmapSlider.setOrientation(QtCore.Qt.Horizontal)
    self.thresholdRoadmapSlider.setObjectName("ThresholdBolusSlider")
    self.thresholdRoadmapSlider.valueChanged.connect(partial(functionThresholdRoadmapSlider, self))
    
    self.thresholdBolusSlider = Qt.QSlider(self)
    self.thresholdBolusSlider.setMaximum(100)
    self.thresholdBolusSlider.setProperty("value", 50)
    self.thresholdBolusSlider.setOrientation(QtCore.Qt.Horizontal)
    self.thresholdBolusSlider.setObjectName("ThresholdBolusSlider")
    self.thresholdBolusSlider.valueChanged.connect(partial(functionThresholdBolusSlider, self) )        
    
    self.label_opacity_bolus_slider = Qt.QLabel(self)        
    self.label_opacity_bolus_slider.setText("Opacity Bolus");   
    self.label_opacity_bolus_slider.setFixedWidth(125) 
    
    self.label_steepness_bolus_slider = Qt.QLabel(self)        
    self.label_steepness_bolus_slider.setText("Steepness Bolus");   
    self.label_steepness_bolus_slider.setFixedWidth(125) 
    
    self.label_steepness_roadmap_slider = Qt.QLabel(self)        
    self.label_steepness_roadmap_slider.setText("Steepness Roadmap");   
    self.label_steepness_roadmap_slider.setFixedWidth(125) 
    
    self.volumeOpacityBolus = Qt.QSlider(self)
    self.volumeOpacityBolus.setMaximum(100)
    self.volumeOpacityBolus.setProperty("value", 50)
    self.volumeOpacityBolus.setOrientation(QtCore.Qt.Horizontal)
    self.volumeOpacityBolus.setObjectName("volumeOpacityBolus")     
    self.volumeOpacityBolus.valueChanged.connect(partial(functionOpacityBolusSlider, self))    
    
    self.label_opacity_roadmap_slider = Qt.QLabel(self)        
    self.label_opacity_roadmap_slider.setText("Opacity Roadmap");   
    self.label_opacity_roadmap_slider.setFixedWidth(125)     
    
    self.volumeOpacityRoadmap = Qt.QSlider(self)
    self.volumeOpacityRoadmap.setMaximum(100)
    self.volumeOpacityRoadmap.setProperty("value", 50)
    self.volumeOpacityRoadmap.setOrientation(QtCore.Qt.Horizontal)
    self.volumeOpacityRoadmap.setObjectName("volumeOpacityRoadmap")        
    self.volumeOpacityRoadmap.valueChanged.connect(partial(functionOpacityRoadmapSlider, self))       
    
    self.label_playback_speed = Qt.QLabel(self)  
    self.label_playback_speed.setText("Playback Speed") 
    self.label_playback_speed.setFixedWidth(125)        
    
    self.playbackSpeedSlider = Qt.QSlider(self)
    self.playbackSpeedSlider.setMaximum(500)
    self.playbackSpeedSlider.setProperty("value", round(self.t_ms))
    self.playbackSpeedSlider.setOrientation(QtCore.Qt.Horizontal)
    self.playbackSpeedSlider.setObjectName("playbackSpeedSlider")    
    self.playbackSpeedSlider.setTickInterval(21.5)
    self.playbackSpeedSlider.setTickPosition(Qt.QSlider.TicksBelow)         
    self.playbackSpeedSlider.valueChanged.connect(partial(setPlaybackSpeed1, self))  

    self.btn_activate_manual_lookup_table_bolus = Qt.QPushButton('', self)
    self.btn_activate_manual_lookup_table_bolus.setText("Define lookup table bolus")    
    self.btn_activate_manual_lookup_table_bolus.\
        clicked.connect( partial(manualLookupTableBolus, self)  )
        
    self.btn_activate_manual_lookup_table_roadmap = Qt.QPushButton('', self)
    self.btn_activate_manual_lookup_table_roadmap.setText("Define lookup table roadmap")    
    self.btn_activate_manual_lookup_table_roadmap.\
        clicked.connect( partial(manualLookupTableRoadmap, self)  )    
    
    self.label_camera_operations = Qt.QLabel()
    self.label_camera_operations.setText("Manual camera control")
    self.label_camera_operations.setStyleSheet('color: grey')
    self.label_camera_operations.setWordWrap(True)
    self.label_camera_operations.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_sliders = Qt.QLabel()
    self.label_text_above_sliders.setText("Quick control lookup table")
    self.label_text_above_sliders.setStyleSheet('color: grey')
    self.label_text_above_sliders.setWordWrap(True)
    self.label_text_above_sliders.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_playback_settings = Qt.QLabel()
    self.label_text_above_playback_settings.setText("Playback control")
    self.label_text_above_playback_settings.setStyleSheet('color: grey')
    self.label_text_above_playback_settings.setWordWrap(True)
    self.label_text_above_playback_settings.setAlignment(Qt.Qt.AlignCenter)    
    
    self.btn_set_camera_position = Qt.QPushButton('Dialog', self)
    self.btn_set_camera_position.move(20, 20)   
    self.btn_set_camera_position.clicked.connect(partial(setCameraPosition, self))
    self.btn_set_camera_position.setText("Set Camera Position")
    
    self.camera_position_x = Qt.QLineEdit(self)
    self.validator_camera_position_x = Qt.QIntValidator()
    self.camera_position_x.setValidator(self.validator_camera_position_x)
    
    self.camera_position_y = Qt.QLineEdit(self)
    self.validator_camera_position_y = Qt.QIntValidator()
    self.camera_position_y.setValidator(self.validator_camera_position_y)
    
    self.camera_position_z = Qt.QLineEdit(self)
    self.validator_camera_position_z = Qt.QIntValidator()
    self.camera_position_z.setValidator(self.validator_camera_position_z)    
    
    self.btn_set_camera_focal_point = Qt.QPushButton('Dialog', self)
    self.btn_set_camera_focal_point.move(20, 20)   
    self.btn_set_camera_focal_point.clicked.connect(partial(setCameraFocalPoint, self))
    self.btn_set_camera_focal_point.setText("Set Camera Focal Point")
    
    self.camera_focal_point_x = Qt.QLineEdit(self)
    self.validator_camera_focal_point_x = Qt.QIntValidator()
    self.camera_focal_point_x.setValidator(self.validator_camera_focal_point_x)
    
    self.camera_focal_point_y = Qt.QLineEdit(self)
    self.validator_camera_focal_point_y = Qt.QIntValidator()
    self.camera_focal_point_y.setValidator(self.validator_camera_focal_point_y)
    
    self.camera_focal_point_z = Qt.QLineEdit(self)
    self.validator_camera_focal_point_z = Qt.QIntValidator()
    self.camera_focal_point_z.setValidator(self.validator_camera_focal_point_z)   
    
    self.camera_rotation_angle = Qt.QLineEdit(self)
    self.validator_camera_rotation_angle = Qt.QIntValidator()
    self.camera_rotation_angle.setValidator(self.validator_camera_rotation_angle)
    
    self.btn_camera_rotate = Qt.QPushButton('Dialog', self)
    self.btn_camera_rotate.move(20, 20)   
    self.btn_camera_rotate.clicked.connect(partial(rotateCamera, self))
    self.btn_camera_rotate.setText("Rotate [°]")   

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
    self.hl_checkboxes.addWidget(self.save_images_checkbox)
    self.hl_checkboxes.addWidget(self.checkbox_FOV)
    self.hl_checkboxes.addWidget(self.roadmap_buildup_checkbox)
    self.hl_checkboxes.addWidget(self.checkbox_scalar_bar)
    self.hl_checkboxes.addWidget(self.checkbox_camera_specifications)    
    
    self.hl_playback_settings = Qt.QHBoxLayout()
    self.hl_playback_settings.addWidget(self.image_count_label)
    self.hl_playback_settings.addWidget(self.image_count_display)
    self.hl_playback_settings.addWidget(self.frame_rate_label)
    self.hl_playback_settings.addWidget(self.frame_rate_display)    
    self.hl_playback_settings.addWidget(self.placeholder)   
    self.hl_playback_settings.addWidget(self.previous_image_button)
    self.hl_playback_settings.addWidget(self.start_stop_button)
    self.hl_playback_settings.addWidget(self.next_image_button)    
    
    self.hl_threshold_bolus = Qt.QHBoxLayout()
    self.hl_threshold_bolus.addWidget(self.label_bolus_slider)
    self.hl_threshold_bolus.addWidget(self.thresholdBolusSlider)    
    
    self.hl_threshold_roadmap = Qt.QHBoxLayout()
    self.hl_threshold_roadmap.addWidget(self.label_roadmap_slider)
    self.hl_threshold_roadmap.addWidget(self.thresholdRoadmapSlider)    
    
    self.hl_opacity_bolus_slider = Qt.QHBoxLayout()
    self.hl_opacity_bolus_slider.addWidget(self.label_opacity_bolus_slider)
    self.hl_opacity_bolus_slider.addWidget(self.volumeOpacityBolus)    
    
    self.hl_opacity_roadmap_slider = Qt.QHBoxLayout()
    self.hl_opacity_roadmap_slider.addWidget(self.label_opacity_roadmap_slider)
    self.hl_opacity_roadmap_slider.addWidget(self.volumeOpacityRoadmap)    
    
    self.hl_steepness_bolus_slider = Qt.QHBoxLayout()
    self.hl_steepness_bolus_slider.addWidget(self.label_steepness_bolus_slider)
    self.hl_steepness_bolus_slider.addWidget(self.steepnessBolusSlider)      
    
    self.hl_steepness_roadmap_slider = Qt.QHBoxLayout()
    self.hl_steepness_roadmap_slider.addWidget(self.label_steepness_roadmap_slider)
    self.hl_steepness_roadmap_slider.addWidget(self.steepnessRoadmapSlider)     
    
    self.hl_playback_speed = Qt.QHBoxLayout()
    self.hl_playback_speed.addWidget(self.label_playback_speed)
    self.hl_playback_speed.addWidget(self.playbackSpeedSlider)    
    
    self.hl_manual_lookup_tables = Qt.QHBoxLayout()
    self.hl_manual_lookup_tables.addWidget(self.btn_activate_manual_lookup_table_bolus)
    self.hl_manual_lookup_tables.addWidget(self.btn_activate_manual_lookup_table_roadmap)     
    
    self.hl_set_camera_position = Qt.QHBoxLayout()
    self.hl_set_camera_position.addWidget(self.camera_position_x)
    self.hl_set_camera_position.addWidget(self.camera_position_y)
    self.hl_set_camera_position.addWidget(self.camera_position_z) 
    self.hl_set_camera_position.addWidget(self.btn_set_camera_position)    
    
    self.hl_set_camera_focal_point = Qt.QHBoxLayout()
    self.hl_set_camera_focal_point.addWidget(self.camera_focal_point_x)
    self.hl_set_camera_focal_point.addWidget(self.camera_focal_point_y)
    self.hl_set_camera_focal_point.addWidget(self.camera_focal_point_z) 
    self.hl_set_camera_focal_point.addWidget(self.btn_set_camera_focal_point)  
  
    self.grid_camera_operations = Qt.QGridLayout()    
    self.grid_camera_operations.addWidget(self.camera_position_x, 1, 2)
    self.grid_camera_operations.addWidget(self.camera_position_y, 1, 3)
    self.grid_camera_operations.addWidget(self.camera_position_z, 1, 4)
    self.grid_camera_operations.addWidget(self.btn_set_camera_position, 1, 1)    
    self.grid_camera_operations.addWidget(self.camera_focal_point_x, 2, 2)
    self.grid_camera_operations.addWidget(self.camera_focal_point_y, 2, 3)
    self.grid_camera_operations.addWidget(self.camera_focal_point_z, 2, 4)
    self.grid_camera_operations.addWidget(self.btn_set_camera_focal_point, 2, 1)    
    self.grid_camera_operations.addWidget(self.btn_camera_rotate, 3, 1)
    self.grid_camera_operations.addWidget(self.camera_rotation_angle, 3, 2)    
    
    # Definition of the vertical and horizontal main axis    
    self.vl_main = Qt.QVBoxLayout()    
    self.hl_main = Qt.QHBoxLayout()      
    self.frame.setLayout(self.hl_main)
    
    # Align all widgets or horizontal layouts along the vertical main axis 
    self.vl_main.addLayout(self.hl_load_buttons)
    self.vl_main.addLayout(self.hl_checkboxes)
    self.vl_main.addWidget(self.diagram_op.canvas)
    self.vl_main.addWidget(self.label_text_above_playback_settings)
    self.vl_main.addLayout(self.hl_playback_settings) 
    self.vl_main.addLayout(self.hl_playback_speed)
    self.vl_main.addWidget(self.placeholder)         
    self.vl_main.addWidget(self.label_text_above_sliders)
    self.vl_main.addLayout(self.hl_threshold_bolus)
    self.vl_main.addLayout(self.hl_threshold_roadmap)
    self.vl_main.addLayout(self.hl_opacity_bolus_slider)
    self.vl_main.addLayout(self.hl_opacity_roadmap_slider)
    self.vl_main.addLayout(self.hl_steepness_bolus_slider)  
    self.vl_main.addLayout(self.hl_steepness_roadmap_slider)  
    self.vl_main.addWidget(self.placeholder)    
    self.vl_main.addLayout(self.hl_manual_lookup_tables)
    self.vl_main.addWidget(self.placeholder)
    self.vl_main.addWidget(self.label_camera_operations)   
    self.vl_main.addLayout(self.grid_camera_operations)    
    
    # Alignment along horizontal main axis   
    self.hl_main.addLayout(self.vl_main, stretch=1 )
    self.hl_main.addWidget(self.vtkWidget, stretch=2)
    
    
        