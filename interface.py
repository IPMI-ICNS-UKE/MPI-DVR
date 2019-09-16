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
import manual_input_color_map



""" 
This file contains the initUI and the functions directly connected to 
the display widgets (e.g. buttons, sliders, ...) 
"""


def enableDisableButtons(self, bool_value):
    for i in self.findChildren(Qt.QPushButton):
        i.setEnabled(bool_value)            
    for i in self.findChildren(Qt.QCheckBox):
        i.setEnabled(bool_value)        
    for i in self.findChildren(Qt.QSlider):
        i.setEnabled(bool_value)
    for i in self.findChildren(Qt.QComboBox):
        i.setEnabled(bool_value)
    for i in self.findChildren(Qt.QLineEdit):
        i.setEnabled(bool_value)

def preImageAnalysisSettings(self):
    index = self.combobox_pre_image_analysis.currentIndex()
    if (index == 0):
        # Pre-image analysis on
        self.bool_create_histogram = self.diag.bool_create_histogram = True
        self.bool_max_min = self.diag.bool_max_min = True
        self.less_images = self.diag.less_images = None
        
    if (index == 1):
        # Only max/min
        self.bool_create_histogram = self.diag.bool_create_histogram = False
        self.bool_max_min = self.diag.bool_max_min = True
        self.less_images = self.diag.less_images = None
        
    if (index == 2): 
        # Restrict to random selection of 100 images
        self.bool_create_histogram =self.diag.bool_create_histogram = True
        self.bool_max_min = self.diag.bool_max_min = True
        self.less_images = self.diag.less_images = 100
    
    if (index == 3):
        # Pre-image analysis off
        
        # In case of reloading new dataset, it is necessary to reset min/max 
        # values to the default settings
        self.min_value = self.default_min_value
        self.max_value = self.default_max_value        
        
        self.bool_create_histogram = self.diag.bool_create_histogram = False
        self.bool_max_min = self.diag.bool_max_min = False
        self.less_images = self.diag.less_images = None   


def setColor(self, name):
    if name == 'bl':
        i = self.combobox_color_bl.currentIndex()
    if name == 'rm':
        i = self.combobox_color_rm.currentIndex()
        
    if (i == 0):
        # Set color red 
        self.vtk_pip.setMonoColor(name, 1, 0, 0)
        
    if (i == 1):
        # Set color blue 
        self.vtk_pip.setMonoColor(name, 0, 0, 1)
        
    if (i == 2):
        self.vtk_pip.setMonoColor(name, 0, 1, 0)     
        
    if (i == 3):
        # Set color map    
        if name == 'bl':
            self.subwindow_color_map_settings_bl.show()
        if name == 'rm':
            self.subwindow_color_map_settings_rm.show()
        
    if (i == 4): 
        if name == 'bl':    
            self.subwindow_color_rgb_bl.show()
        if name == 'rm':    
            self.subwindow_color_rgb_rm.show() 
    
           
            
        

def resetSlidersToStartPosition(self):
    self.slider_intervall_ramp_rm.setProperty("value", 10000*self.sl_pos_ri_rm)
    self.slider_intervall_ramp_bl.setProperty("value", 10000*self.sl_pos_ri_bl)
    self.slider_th_bl.setProperty("value", 100*self.sl_pos_th_bl)
    self.slider_th_rm.setProperty("value", 100*self.sl_pos_th_rm)
    self.slider_op_bl.setProperty("value", 100*self.sl_pos_op_bl)
    self.slider_op_rm.setProperty("value", 100*self.sl_pos_op_bl)
    
def setCameraOperation(self):
    le_input = self.lineedit_camera_control.text()
    i = self.combobox_box_camera.currentIndex()
    
    if i == 0:   # Set camera pos        
        try:  
            coords_str = le_input.split(",")             
            x = float(coords_str[0])
            y = float(coords_str[1])
            z = float(coords_str[2])            
    
            self.vtk_pip.setCameraPosition(x, y, z)    
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
            
            self.vtk_pip.setCameraFocalPoint(x, y, z)   
            
            self.displayPos()    
            self.iren.Initialize()
            self.iren.Start()   
        except:
            print("Type in coordinates in correct form: x,y,z")
        
    if i == 2:   # Set rotation
        try: 
            rotation_angle = int(le_input  )
            camera = self.vtk_pip.ren.GetActiveCamera()
            camera.Roll(rotation_angle)    
            self.displayPos()    
            self.iren.Initialize()
            self.iren.Start()     
        except:
            print("Type in angle rotation in correct form!")
            
def setAmbDiffSpec(self, name):        
    if name == 'bl': 
        le = self.lineedit_amb_diff_spec_bl
        vp = self.vtk_pip.volumePropertyBl
    if name == 'rm':
        le = self.lineedit_amb_diff_spec_rm
        vp = self.vtk_pip.volumePropertyRm
        
    i = self.combobox_amb_diff_spec.currentIndex()
    le_input = le.text()
    
    if i == 1:   # Set ambient       
        try:  
            le.setPlaceholderText(str(le_input))
            vp.SetAmbient(float(le_input))
            self.iren.Initialize()
            self.iren.Start()
        except:
            print("Type in valid value!")
        
    if i == 2:   # Set diffuse        
        try:       
            le.setPlaceholderText(str(le_input))
            vp.SetDiffuse(float(le_input))
            self.iren.Initialize()
            self.iren.Start()
        except:
            print("Type in valid value!")
            
    if i == 3: 
        try: 
            le.setPlaceholderText(str(le_input))
            vp.SetSpecular(float(le_input))
            self.iren.Initialize()
            self.iren.Start()   
        except:
            print("Type in valid value!")
            
def placeholderLineEditAmbDiffSpec(self, name, i):
    if name == 'bl': 
        le = self.lineedit_amb_diff_spec_bl
        vp = self.vtk_pip.volumePropertyBl
    if name == 'rm':
        le = self.lineedit_amb_diff_spec_rm
        vp = self.vtk_pip.volumePropertyRm
        
    if i == 1:   # Get currrent amb value        
        a = vp.GetAmbient()
        le.clear()
        le.setPlaceholderText(str(a))           
        
    if i == 2:   # Set focal point  
        a = vp.GetDiffuse()
        le.clear()           
        le.setPlaceholderText(str(a))           
        
    if i == 3:   # Set angle
        a = vp.GetSpecular()
        le.clear()
        le.setPlaceholderText(str(a))  


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
    self.vtk_pip.setCameraPosition(x, y, z)    
    self.displayPos()    
    self.iren.Initialize()
    self.iren.Start()     
    
def setCameraFocalPoint(self):    
    x = int( self.camera_focal_point_x.text() )
    y = int( self.camera_focal_point_y.text() )
    z = int( self.camera_focal_point_z.text() )    
    self.vtk_pip.setCameraFocalPoint(x, y, z)    
    self.displayPos()    
    self.iren.Initialize()
    self.iren.Start()     
    
def rotateCamera(self):     
    rotation_angle = int( self.camera_rotation_angle.text() )
    camera = self.vtk_pip.ren.GetActiveCamera()    
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
            self.vtk_pip.dimensions_vtk_data = self.dims            
            
            self.vtk_pip.adjustSizeRm(self.dims, self.checkbox_rm_buildup.isChecked())
            self.image_count = self.image_count - 1
            self.updateStatus()
            
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
        self.vtk_pip.dimensions_vtk_data = self.dims_original
        
        # Resize rm matrix    
        self.vtk_pip.adjustSizeRm(self.dims_original, self.checkbox_rm_buildup.isChecked())
        self.image_count = self.image_count - 1
        self.updateStatus()
        
        #Update image size on UI display
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
        self.label_display_image_data_size.setText(image_size_text)
        
        self.iren.Initialize()
        self.iren.Start()           
 
def manualLookupTablebl(self):  
    self.subwindow_lookup_table_bl.show()       
        
def manualLookupTablerm(self):  
    self.subwindow_lookup_table_rm.show()        

def functionSliderThRm(self, t):
    scale_factor = ( self.max_value - self.min_value ) / 100.0    
    self.th_rm = self.min_value + t  * scale_factor    
    self.diag.th_rm = self.th_rm
    self.diag.manual_lookup_table_rm = False
    self.diag.drawLookupTable()        
    self.vtk_pip.updateThRm(self.th_rm)     
    
def functionSliderThBl(self, t):
    scale_factor = ( self.max_value - self.min_value ) / 100.0    
    self.th_bl = self.min_value + t  * scale_factor    
    self.diag.th_bl = self.th_bl
    self.diag.manual_lookup_table_bl = False
    self.diag.drawLookupTable()     
    self.vtk_pip.updateThBl(self.th_bl)        
    
def functionSliderRampIntervallBl(self, t):
    scale_factor = ( self.max_value - self.min_value) / 10000.0
    self.ri_bl = t * scale_factor      
    self.diag.ri_bl = self.ri_bl
    self.diag.manual_lookup_table_bl = False
    self.diag.drawLookupTable()        
    self.vtk_pip.updateRampIntervallBl(self.ri_bl)
    
def functionSliderRampIntervallRm(self, t):
    scale_factor = ( self.max_value - self.min_value ) / 10000.0
    self.ri_rm =  t * scale_factor    
    self.diag.ri_rm = self.ri_rm
    self.diag.manual_lookup_table_rm = False
    self.diag.drawLookupTable()    
    self.vtk_pip.updateRampIntervallRm(self.ri_rm)

def functionSliderOpBl(self, t):
    self.op_max_bl = t / 100.0    
    self.diag.op_max_bl = self.op_max_bl
    self.diag.manual_lookup_table_bl = False
    self.diag.drawLookupTable()    
    self.vtk_pip.updateOpBl(self.op_max_bl)
    
def functionSliderOpRm(self, t):
    self.op_max_rm = t / 100.0    
    self.diag.op_max_rm = self.op_max_rm
    self.diag.manual_lookup_table_rm = False
    self.diag.drawLookupTable()    
    self.vtk_pip.updateOpRm(self.op_max_rm)    

def checkboxShowRoadmap(self):      
    """ 
    Function shows / hides the rm depending on the status 
    of the corresponding checkbox
    """    
    if not self.checkbox_rm_buildup.isChecked():                             
        self.vtk_pip.volumeMapperRm.SetInputData(self.vtk_pip.createEmptyImageData())         
        self.iren.Initialize()
        self.iren.Start()
    else:
        self.vtk_pip.rmBuildup(self.temporary_image)
        self.iren.Initialize()
        self.iren.Start()
        
def checkboxFOVFunction(self):
    """
    Function shows / hides the FOV of the image 
    depending on the status (checked / unchecked) of the corresponding 
    checkbox
    """
    if not self.checkbox_FOV.isChecked():                                      
        self.vtk_pip.ren.RemoveActor(self.vtk_pip.grid) 
        self.iren.Initialize()
        self.iren.Start()
    else:
        self.vtk_pip.grid = self.vtk_pip.createGrid()
        self.vtk_pip.ren.AddActor(self.vtk_pip.grid)
        self.iren.Initialize()
        self.iren.Start()
        
def checkboxCameraSpecifications(self):
    """
    Function shows / hides current camera position, focal point and
    rotation
    """
    if not self.checkbox_camera_specifications.isChecked():                                      
        self.vtk_pip.ren.RemoveActor(self.vtk_pip.text_actor) 
        self.iren.Initialize()
        self.iren.Start()
    else:        
        self.vtk_pip.ren.AddActor(self.vtk_pip.text_actor)
        self.iren.Initialize()
        self.iren.Start()

def setPlaybackSpeed1(self, t):
    """ 
    Function gets input t from the QT slider and  
    updates the Qt timer resulting in a modified 
    playback speed. Unit of t_ms is milliseconds.
    """
    self.t_ms = t    
    self.timer.start(self.t_ms)
    if not self.button_start_stop.isChecked(): 
        self.timer.stop()     
        
def computeHistogramDataBin(self, directory, mode):    
    """
    This function gathers image values of the dataset in order 
    to create a data bin that is used for histogram visualization. 
    """       
    self.data_bin = []         
    if mode == 'mdf':                        
        self.data_bin = self.diag.data_bin = mdf_reader.returnDataArray(directory, \
        self.bool_create_histogram, self.bool_max_min, self.less_images)             
    if mode == 'mha':  
        self.data_bin = self.diag.data_bin = mha_reader.returnDataArray(directory, \
        self.bool_create_histogram, self.bool_max_min, self.less_images)
        
    if self.bool_max_min == True:
        self.max_value  = max(self.data_bin)
        self.min_value = min(self.data_bin)        

    
def loadMHA(self):        
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')        
    name = fname + "/1.mha"     
    if os.path.isfile(name):
        preImageAnalysisSettings(self)
        self.source_data_format = 'mha'
        self.directory_mha = fname
        self.number_of_total_images =  mha_reader.getNumberImages(self.directory_mha)   
        self.dims = mha_reader.returnDimsFirstImage(self.directory_mha) 
        self.spacing = mha_reader.returnSpacingFirstImage(self.directory_mha) 
        self.dims_original = self.dims
        self.rm_counter = 0
        self.screenshot_number = 0
        
        # Counter for images and screenshots
        self.image_count = 0                
        self.rm_counter = 0
        
        # Use of manual lookup tables
        self.manual_lookup_table_bl = None
        self.manual_lookup_table_rm = None        
        
        # Create data bin (if pre image analysis settings active)
        computeHistogramDataBin(self, self.directory_mha, 'mha')
        
        # Values are used to update the value range of the slider widgets
        self.updateVisualizationParameters()      
       
        # Create histogram from data bin (if pre image analysis settings 
        # active) and draw look up table 
        self.diag.drawHistogram()   
        self.diag.drawLookupTable()
          
        # Create internal look up table for VTK pipeline                       
        self.vtk_pip.updateVTKparameters(self.dims, self.spacing)
        
        # Update image count and image size display
        image_count = '1 / '+ str(self.number_of_total_images)      
        self.label_image_count_display.setText(image_count)  
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+'x'+str(self.dims[2])
        self.label_display_image_data_size.setText(image_size_text)
        
        # Enable all UI buttons, sliders and checkboxes
        resetSlidersToStartPosition(self)
        enableDisableButtons(self,True) 
        self.updateStatus()
    else: 
        print("Use valid directory")        

def loadMDF(self):    
    fname = Qt.QFileDialog.getOpenFileName(self, 'c:\\')[0]       
    if fname != '':
        preImageAnalysisSettings(self)
        self.source_data_format = 'mdf'
        self.directory_mdf = fname
        self.image_count = 0
        self.screenshot_number = 0
        self.rm_counter = 0
        
        # Use of manual lookup tables
        self.manual_lookup_table_bl = None
        self.manual_lookup_table_rm = None
        
        # Get number of images and image size
        self.number_of_total_images = mdf_reader.getNumberImages(self.directory_mdf)
        self.dims = mdf_reader.returnDimensionsImageData(self.directory_mdf) 
        self.spacing = mdf_reader.returnSpacingImageData(self.directory_mdf) 
        
        # Variable to save original dims, if interpolation option is activated
        self.dims_original = self.dims        
        
        # Create data bin and determine image value range
        computeHistogramDataBin(self, self.directory_mdf, 'mdf')  
        
        # Values are used to update the value range of the slider widgets
        self.updateVisualizationParameters() 
        
        # Create histogram
        self.diag.drawHistogram()  
        self.diag.drawLookupTable() 
        
        # Create internal look up table for VTK pipeline                  
        self.vtk_pip.updateVTKparameters(self.dims, self.spacing)
        
        # Update image count and image size display
        image_count = '1 / '+ str(self.number_of_total_images)        
        self.label_image_count_display.setText(image_count)  
        image_size_text = str(self.dims[0])+'x'+str(self.dims[1])+ \
                              'x'+str(self.dims[2]) 
        self.label_display_image_data_size.setText(image_size_text)
        
        # Enable all UI buttons, sliders and checkboxes
        resetSlidersToStartPosition(self)
        enableDisableButtons(self, True) 
        
        # Time stamps are used for computation of real frame rate    
        self.updateStatus()
        
def setScreenshotSaveDirectory(self):
    """
    Function opens a simple diaglogue window to select a directory, where 
    subsequently captured screenshots can be saved
    """    
    fname = Qt.QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\')         
    self.directory_output = fname     
    self.checkbox_save_images.setChecked(True)    

        
def pauseAndPlay(self, pressed):     
    if pressed:
        self.timer.start(self.t_ms)
        self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPause))
    else:             
        self.timer.stop()
        self.label_frame_rate_display.setText('-')
        self.button_start_stop.setIcon(self.style().standardIcon(Qt.QStyle.SP_MediaPlay))        
    
def showNextImage(self):    
    self.image_count = self.image_count + 1        
    if self.image_count > self.number_of_total_images:
        self.image_count = 1           
    if self.source_data_format == 'mha':            
        self.temporary_image = \
        mha_reader.createVTKDataFromMHAFile(self.directory_mha, \
                                      self.image_count, self.interpolation, \
                                      self.dims)          
    if self.source_data_format == 'mdf':            
        self.temporary_image = mdf_reader.createVTKDataFromHDF(self.directory_mdf, \
                                 self.image_count-1, self.interpolation, \
                                 self.dims)        
    self.vtk_pip.volumeMapperBl.SetInputData(self.temporary_image)       
    if self.checkbox_rm_buildup.isChecked() and \
    self.rm_counter < self.number_of_total_images: 
        self.vtk_pip.rmBuildup(self.temporary_image) 
        self.rm_counter = self.rm_counter+1
        
    # Save screenshots of visualized MPI data
    if self.checkbox_save_images.isChecked():
        screenshotAndSave(self)               
    self.iren.Initialize()
    self.iren.Start()    
    
    # Update image count display
    image_count = str(self.image_count) + ' / ' + str(self.number_of_total_images)
    self.label_image_count_display.setText(str(image_count) )
    
def showPreviousImage(self):
    self.image_count = self.image_count - 1     
    if self.image_count == 0:        
        self.image_count = self.number_of_total_images 
        
    if self.source_data_format == 'mha':            
        self.temporary_image = mha_reader.createVTKDataFromMHAFile(self.directory_mha, self.image_count, self.interpolation, self.dims)
        
    if self.source_data_format == 'mdf':            
        self.temporary_image = mdf_reader.createVTKDataFromHDF(self.directory_mdf, self.image_count-1, self.interpolation, self.dims)        
    
    self.vtk_pip.volumeMapperBl.SetInputData(self.temporary_image)     
    self.rm_counter = self.rm_counter-1
    
    # Save screenshots of visualized MPI data
    if self.checkbox_save_images.isChecked():
        screenshotAndSave(self)     
    
    self.iren.Initialize()
    self.iren.Start()    

    # Update image count display
    image_count = str(self.image_count) + ' / ' + str(self.number_of_total_images)
    self.label_image_count_display.setText(str(image_count) )
        
def checkOutputDirectory(self):    
    if self.directory_output != None:        
        print('Images will be saved to: ', self.directory_output)        
    else:         
        if self.source_data_format == 'mha':
            path_to_source = os.path.normpath(self.directory_mha)            
        if self.source_data_format == 'mdf':
            path_to_source = os.path.normpath(self.directory_mdf)            
            path_to_source = os.path.dirname(os.path.realpath(path_to_source))        
        temp_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mydir = os.path.join(path_to_source, temp_time)
        os.makedirs(mydir)        
        self.directory_output = path_to_source + "/" + temp_time
        print('No output adress was given. Images will be saved to: ', self.directory_output)         
        
def screenshotAndSave(self):    
    """ 
    Function saves PNG image of current visualization screen to a defined directory. 
    If no directory is given, a new folder (name composed of current date and time) 
    will be created in the source directory. 
    """
    checkOutputDirectory(self)
    if (os.path.isdir(self.directory_output)):
        name_output = "/%d.png" %self.screenshot_number
        string_directory = self.directory_output + name_output
        self.vtk_pip.saveScreenshot(string_directory)
        self.screenshot_number = self.screenshot_number + 1
    
def saveRoapmap(self):        
    fileName, _ = Qt.QFileDialog.getSaveFileName(self, \
     "QFileDialog.getSaveFileName()","","Input Files(*.mha)")       
    self.vtk_pip.writer_rm.SetInputData(self.vtk_pip.image_data_rm)
    self.vtk_pip.writer_rm.SetFileName(fileName)
    self.vtk_pip.writer_rm.Write()   

    
    
    
   
def initUI(self):
    """ 
    This function defines the architecture of the GUI and connects 
    the created QT widgets to the corresponding functions defined in this 
    file. The various QT objects are arranged along vertical and horizontal
    axes.   
    """ 
    
    self.subwindow_color_map_settings_bl = manual_input_color_map.ColorMapSettingsView(self, 'bl')
    self.subwindow_color_map_settings_rm = manual_input_color_map.ColorMapSettingsView(self, 'rm')
    self.subwindow_color_rgb_bl = manual_input_color_map.InputColorRGB(self, 'bl')
    self.subwindow_color_rgb_rm = manual_input_color_map.InputColorRGB(self, 'rm')
    
    self.subwindow_lookup_table_bl = manual_input_lookup_table.TableView(self, 'bl')
    self.subwindow_lookup_table_rm = manual_input_lookup_table.TableView(self, 'rm')
    
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
    
    self.checkbox_rm_buildup = Qt.QCheckBox("Roadmap build-up", self)
    self.checkbox_rm_buildup.setChecked(True)
    self.checkbox_rm_buildup.stateChanged.connect(partial(checkboxShowRoadmap, self))
    

    
    self.checkbox_FOV = Qt.QCheckBox("Show FOV", self)
    self.checkbox_FOV.setChecked(False)
    self.checkbox_FOV.stateChanged.connect(partial(checkboxFOVFunction, self))
    
    self.checkbox_camera_specifications = Qt.QCheckBox("Show camera specifications", self)
    self.checkbox_camera_specifications.setChecked(True)
    self.checkbox_camera_specifications.stateChanged.connect(partial(checkboxCameraSpecifications, self))  
   
    self.button_save_rm = Qt.QPushButton('Save roadmap')
    self.button_save_rm.clicked.connect( partial(saveRoapmap, self) )     
    
    self.checkbox_save_images = Qt.QCheckBox("Save screenshots", self)
    self.checkbox_save_images.setChecked(False)
    self.checkbox_save_images.stateChanged.connect(partial(screenshotAndSave, self)) 

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

    self.label_th_slider = Qt.QLabel(self)        
    self.label_th_slider.setText("Threshold")   
    self.label_th_slider.setFixedWidth(125) 
    
    self.slider_intervall_ramp_rm = Qt.QSlider(self)
    self.slider_intervall_ramp_rm.setMinimum(1)
    self.slider_intervall_ramp_rm.setMaximum(10000)
    self.slider_intervall_ramp_rm.setProperty("value", 10000*self.sl_pos_ri_rm)
    self.slider_intervall_ramp_rm.setOrientation(QtCore.Qt.Horizontal)
    self.slider_intervall_ramp_rm.setObjectName("slider_intervall_ramp_rm")
    self.slider_intervall_ramp_rm.valueChanged.connect(partial(functionSliderRampIntervallRm, self))  
    
    self.slider_intervall_ramp_bl = Qt.QSlider(self)
    self.slider_intervall_ramp_bl.setMinimum(1)
    self.slider_intervall_ramp_bl.setMaximum(10000)
    self.slider_intervall_ramp_bl.setProperty("value", 10000*self.sl_pos_ri_bl)
    self.slider_intervall_ramp_bl.setOrientation(QtCore.Qt.Horizontal)
    self.slider_intervall_ramp_bl.setObjectName("slider_th_bl")
    self.slider_intervall_ramp_bl.valueChanged.connect(partial(functionSliderRampIntervallBl, self) )  
            
    self.slider_th_rm = Qt.QSlider(self)
    self.slider_th_rm.setMaximum(100)    
    self.slider_th_rm.setProperty("value", 100*self.sl_pos_th_rm)
    self.slider_th_rm.setOrientation(QtCore.Qt.Horizontal)
    self.slider_th_rm.setObjectName("slider_th_bl")
    self.slider_th_rm.valueChanged.connect(partial(functionSliderThRm, self))
    
    self.slider_th_bl = Qt.QSlider(self)
    self.slider_th_bl.setMaximum(100)    
    self.slider_th_bl.setProperty("value", 100*self.sl_pos_th_bl)
    self.slider_th_bl.setOrientation(QtCore.Qt.Horizontal)
    self.slider_th_bl.setObjectName("slider_th_bl")
    self.slider_th_bl.valueChanged.connect(partial(functionSliderThBl, self) )        
    
    self.label_op_slider = Qt.QLabel(self)        
    self.label_op_slider.setText("Opacity")   
    self.label_op_slider.setFixedWidth(125) 
    
    self.label_intervall_ramp_ramp = Qt.QLabel(self)        
    self.label_intervall_ramp_ramp.setText("Intervall ramp");   
    self.label_intervall_ramp_ramp.setFixedWidth(125)    
    
    self.slider_op_bl = Qt.QSlider(self)
    self.slider_op_bl.setMaximum(100)
    self.slider_op_bl.setProperty("value", 100*self.sl_pos_op_bl)
    self.slider_op_bl.setOrientation(QtCore.Qt.Horizontal)
    self.slider_op_bl.setObjectName("slider_op_bl")     
    self.slider_op_bl.valueChanged.connect(partial(functionSliderOpBl, self))    
    
    self.slider_op_rm = Qt.QSlider(self)
    self.slider_op_rm.setMaximum(100)
    self.slider_op_rm.setProperty("value", 100*self.sl_pos_op_rm)
    self.slider_op_rm.setOrientation(QtCore.Qt.Horizontal)
    self.slider_op_rm.setObjectName("slider_op_rm")        
    self.slider_op_rm.valueChanged.connect(partial(functionSliderOpRm, self))       
    
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

    self.button_activate_manual_lookup_table_bl = Qt.QPushButton('', self)
    self.button_activate_manual_lookup_table_bl.setText("Define lookup table bolus")    
    self.button_activate_manual_lookup_table_bl.\
        clicked.connect( partial(manualLookupTablebl, self)  )
        
    self.button_activate_manual_lookup_table_rm = Qt.QPushButton('', self)
    self.button_activate_manual_lookup_table_rm.setText("Define lookup table roadmap")    
    self.button_activate_manual_lookup_table_rm.\
        clicked.connect( partial(manualLookupTablerm, self)  )    
    
    self.label_camera_operations = Qt.QLabel()
    self.label_camera_operations.setText("Manual camera control")
    self.label_camera_operations.setStyleSheet('color: grey')
    self.label_camera_operations.setWordWrap(True)
    self.label_camera_operations.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_manual_defintion_lookup_table = Qt.QLabel()
    self.label_manual_defintion_lookup_table.setText("Manual definition")  
    self.label_manual_defintion_lookup_table.setWordWrap(True)   
    
    self.label_text_above_bl_slider = Qt.QLabel()
    self.label_text_above_bl_slider.setText("Bolus")
    self.label_text_above_bl_slider.setStyleSheet('color: grey')    
    self.label_text_above_bl_slider.setAlignment(Qt.Qt.AlignCenter)
    
    self.label_text_above_rm_slider = Qt.QLabel()
    self.label_text_above_rm_slider.setText("Roadmap")
    self.label_text_above_rm_slider.setStyleSheet('color: grey')    
    self.label_text_above_rm_slider.setAlignment(Qt.Qt.AlignCenter)
    
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
    
    self.button_set_amb_diff_spec_rm = Qt.QPushButton('Dialog', self)   
    self.button_set_amb_diff_spec_rm.clicked.connect(partial(setAmbDiffSpec, self, 'rm'))
    self.button_set_amb_diff_spec_rm.setText("SET")   
    
    self.button_set_amb_diff_spec_bl = Qt.QPushButton('Dialog', self)   
    self.button_set_amb_diff_spec_bl.clicked.connect(partial(setAmbDiffSpec, self, 'bl'))
    self.button_set_amb_diff_spec_bl.setText("SET")   
    
    self.lineedit_camera_control = Qt.QLineEdit(self)
    self.lineedit_camera_control.setPlaceholderText('x, y, z')  
    
    self.lineedit_amb_diff_spec_rm = Qt.QLineEdit(self)    
    self.lineedit_amb_diff_spec_rm.setMinimumSize(10, 10)
    self.lineedit_amb_diff_spec_rm.setSizePolicy(Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Minimum)
    
    self.lineedit_amb_diff_spec_bl = Qt.QLineEdit(self)    
    self.lineedit_amb_diff_spec_bl.setMinimumSize(10, 10)
    self.lineedit_amb_diff_spec_bl.setSizePolicy(Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Minimum)
    
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
   
    self.combobox_amb_diff_spec = Qt.QComboBox()  
    self.combobox_amb_diff_spec.addItem("Lighting...")
    self.combobox_amb_diff_spec.addItem("Set Ambient")
    self.combobox_amb_diff_spec.addItem("Set Diffuse")
    self.combobox_amb_diff_spec.addItem("Set Specular")
    self.combobox_amb_diff_spec.model().item(0).setEnabled(False)    
    self.combobox_amb_diff_spec.currentIndexChanged.connect(partial(placeholderLineEditAmbDiffSpec, self, 'rm'))
    self.combobox_amb_diff_spec.currentIndexChanged.connect(partial(placeholderLineEditAmbDiffSpec, self, 'bl'))
    
    self.combobox_color_bl = Qt.QComboBox()      
    self.combobox_color_bl.addItem("Red")
    self.combobox_color_bl.addItem("Blue")
    self.combobox_color_bl.addItem("Green")
    self.combobox_color_bl.addItem("Activate colormap")
    self.combobox_color_bl.addItem("Enter RGB ...")
    self.combobox_color_bl.currentIndexChanged.connect(partial(setColor, self, 'bl'))
     
    self.combobox_color_rm = Qt.QComboBox()   
    self.combobox_color_rm.addItem("Red")   
    self.combobox_color_rm.addItem("Blue")    
    self.combobox_color_rm.addItem("Green")
    self.combobox_color_rm.addItem("Activate colormap")
    self.combobox_color_rm.addItem("Enter RGB ...")
    self.combobox_color_rm.setCurrentIndex(1)
    self.combobox_color_rm.activated.connect(partial(setColor, self, 'rm'))
    
    self.combobox_pre_image_analysis = Qt.QComboBox()   
    self.combobox_pre_image_analysis.addItem("Pre-image analysis active")   
    self.combobox_pre_image_analysis.addItem("Only max/min")    
    self.combobox_pre_image_analysis.addItem("Restrict to 100 images (random selection)")
    self.combobox_pre_image_analysis.addItem("Pre-image analysis deactivated")    
    self.combobox_pre_image_analysis.setCurrentIndex(0)
    self.combobox_pre_image_analysis.activated.connect(partial(preImageAnalysisSettings, self))
    
    self.label_color = Qt.QLabel(self)        
    self.label_color.setText("Color")   
    self.label_color.setFixedWidth(125)  

    """
    The following lines define the spatial relation of the defined QT widgets 
    along horizontal and vertical axes (--> Qt.QHBoxLayout / Qt.QVBoxLayout)
    """
    
    

    self.hl_load_buttons = Qt.QHBoxLayout()
    self.hl_load_buttons.addWidget(self.button_load_mha_files)
    self.hl_load_buttons.addWidget(self.button_load_mdf_file)    
    self.hl_load_buttons.addWidget(self.button_saving_directory_screenshots)    
    self.hl_load_buttons.addWidget(self.button_save_rm) 
    self.hl_load_buttons.addWidget(self.combobox_pre_image_analysis  )  
    
    self.hl_checkboxes = Qt.QHBoxLayout()
    self.hl_checkboxes.addWidget(self.checkbox_save_images)
    self.hl_checkboxes.addWidget(self.checkbox_FOV)
    self.hl_checkboxes.addWidget(self.checkbox_rm_buildup)    
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
    self.hl_manual_lookup_tables.addWidget(self.button_activate_manual_lookup_table_bl)
    self.hl_manual_lookup_tables.addWidget(self.button_activate_manual_lookup_table_rm)   
        
    self.slider_block = Qt.QGridLayout()    
    self.slider_block.addWidget(self.label_text_above_bl_slider, 1, 2, 1, 2)
    self.slider_block.addWidget(self.label_text_above_rm_slider, 1, 4, 1, 2)  
    
    self.slider_block.addWidget(self.label_color, 4, 1)
    self.slider_block.addWidget(self.combobox_color_bl, 4, 2, 2, 2)
    self.slider_block.addWidget(self.combobox_color_rm, 4, 4, 2, 2)    
    
    self.slider_block.addWidget(self.label_th_slider, 6, 1)
    self.slider_block.addWidget(self.slider_th_bl, 6, 2, 2, 2)
    self.slider_block.addWidget(self.slider_th_rm, 6, 4, 2, 2)       
    self.slider_block.addWidget(self.label_op_slider, 8, 1)
    self.slider_block.addWidget(self.slider_op_bl, 8, 2, 2,2)
    self.slider_block.addWidget(self.slider_op_rm, 8, 4, 2, 2)    
    self.slider_block.addWidget(self.label_intervall_ramp_ramp, 10, 1)    
    self.slider_block.addWidget(self.slider_intervall_ramp_bl, 10, 2, 2, 2)
    self.slider_block.addWidget(self.slider_intervall_ramp_rm, 10, 4, 2, 2)     
    self.slider_block.addWidget(self.label_manual_defintion_lookup_table, 12, 1)    
    self.slider_block.addWidget(self.button_activate_manual_lookup_table_bl, 12, 2, 1, 2)
    self.slider_block.addWidget(self.button_activate_manual_lookup_table_rm, 12, 4, 1, 2)  
    self.slider_block.addWidget(self.combobox_amb_diff_spec, 14, 1) 
    self.slider_block.addWidget(self.lineedit_amb_diff_spec_bl, 14, 2, 1, 1) 
    self.slider_block.addWidget(self.button_set_amb_diff_spec_bl, 14, 3, 1, 1) 
    self.slider_block.addWidget(self.lineedit_amb_diff_spec_rm, 14, 4, 1, 1) 
    self.slider_block.addWidget(self.button_set_amb_diff_spec_rm, 14, 5, 1, 1)     
    
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
    self.vl_main.addWidget(self.diag.canvas)
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
    
    
        