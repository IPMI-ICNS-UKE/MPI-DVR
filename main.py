# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:07:58 2018

@author: domdo
"""

import sys
from PyQt5 import Qt
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from mdf_reader import create_VTK_data_from_HDF
from mha_reader import create_VTK_data_from_mha_file
from diagram_class import plotDiagrams
import interface
from vtk_class import vtk_pipeline

class MainWindow(Qt.QMainWindow):
    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent) 
        
        # Adjust window size        
        self.resize(1400, 900)    
        
        # Time per image; playback speed is intitially set to this 
        # value but can be changed during visualization using the playback 
        # speed slider and the play/pause button. CAVE: a frame rate 
        # of 21.5ms can only be achieved using a very dedicated hardware setup
        self.t_ms = 21.5    
        
        # Dimension of vtk image data to be visualized. The source data 
        # will be interpolated to this size if variable "interpolation" is set to true,
        # otherwise original image dimensions of source will be used
        self.interpolation = False
        self.dims = [25, 25, 25]    
   
        # Image count for screenshots of visualization screen
        self.screenshot_number = 1  
        self.count = 0  
    
        self.previous_time = time.time()        
        self.directory_source = ""
        self.directory_output = ""  
        self.directory_mdf = ""
              

        # Number of total images to be visualized, will be computed automatically 
        self.number_of_total_images = None
        # Data format of source file 
        self.format = 'no_source'     
        
        # Create diagram class objects to draw lookup table curve and 
        # compute+draw image value histogram
        self.diagram_op = plotDiagrams() 
        

        # Create timer in order to constantly update VTK pipeline.
        # Timer can be paused / started via the QT pause / play button
        self.timer = Qt.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_status)    
        
        # Creation of vtk class object to invoke the buildup
        # of visualization pipeline
        self.vtk_op = vtk_pipeline()     
        #self.vtk_op.dimension_vtk_data = self.dims
   
        # Use of manual lookup tables
        self.manual_lookup_table_bolus = None
        self.manual_lookup_table_roadmap = None
            
        # Create QT display interfaces that show visualization pipeline óutput             
        self.frame = Qt.QFrame()      
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)        
        self.setCentralWidget(self.frame)        

        # Setup of QT GUI
        interface.initUI(self)
        
        # Connect VTK pipeline renderer to QT frame display 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.vtk_op.ren)        
       
        # Disable all interface widgets until source data is successfully loaded 
        # (except load buttons)
        self.enableDisableButtons(False)        
        self.button_load_mdf_file.setEnabled(True)
        self.button_load_mha_files.setEnabled(True)
        self.button_saving_directory_screenshots.setEnabled(True)        
        
        # Set main window visible and access render window interactor
        self.show()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.vtk_op.iren = self.iren 
        self.iren.Initialize()
        self.iren.Start()     
        
        # Start timer that constantly updates camera position und focal point
        self.timer_cp = Qt.QTimer(self)
        self.timer_cp.setSingleShot(False)
        self.timer_cp.timeout.connect(self.displayPos) 
        self.timer_cp.start(1)
        
        
    def update_status(self): 
        """
        This function updates the VTK pipeline by feeding the 
        volumeMapperBolus object the subsequent image data object.
        It will be constantly invoked by the QT timer object. 
        The corresponding image data is aquired using the mdf / mha reader.         
        """        
        # Defines number of image that will be visualized
        self.count = self.count + 1 
        # Reset image count if out of boundary 
        # --> Image sequence restarts from the beginning 
        if self.count > self.number_of_total_images:
            self.count = 1             
  
        if self.format == 'mha':            
            self.temporary_image = create_VTK_data_from_mha_file(self.directory_source, self.count, self.interpolation, self.dims)
            
        if self.format == 'mdf':            
            self.temporary_image = create_VTK_data_from_HDF(self.directory_mdf, self.count-1, self.interpolation, self.dims)           
        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)        
        
        if self.roadmap_buildup_checkbox.isChecked(): 
            self.vtk_op.roadmap_buildup(self.temporary_image) 
                
        # Computation of real frame rate        
        self.frame_rate_display.setText(str(round(1.0 / (time.time() - self.previous_time), 2)))
        self.previous_time = time.time()   
        
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.image_count_display.setText(str(image_count) )
        
        # Save screenshots of visualized MPI data if checked
        if self.save_images_checkbox.isChecked():
            interface.screenshot_and_save(self)  
            
        self.iren.Initialize()
        self.iren.Start()    
    
    def displayPos(self):        
        pos = self.vtk_op.ren.GetActiveCamera().GetPosition()
        fp = self.vtk_op.ren.GetActiveCamera().GetFocalPoint()
        text = 'Camera: ' + str( round(pos[0], 1)) + ', ' + str( round(pos[1], 1)) + ', ' \
            + str( round(pos[2], 1)) + ' \nFocal point: ' + str( round(fp[0], 1)) + ', '  \
            + str( round(fp[1], 1)) + ', ' \
            + str( round(fp[2], 1))         
        self.vtk_op.text_actor.SetInput( text )
        self.vtk_op.text_actor.SetPosition ( 20, 20 )
        self.vtk_op.text_actor.GetTextProperty().SetFontSize (24 )
        self.vtk_op.text_actor.GetTextProperty().SetColor ( 0.8, 0.8, 0.8 )
        self.vtk_op.text_actor.GetTextProperty().SetOpacity ( 0.8)
    
    def enableDisableButtons(self, bool_value):
        for i in self.findChildren(Qt.QPushButton):
            i.setEnabled(bool_value)            
        for i in self.findChildren(Qt.QCheckBox):
            i.setEnabled(bool_value)        
        for i in self.findChildren(Qt.QSlider):
            i.setEnabled(bool_value)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())