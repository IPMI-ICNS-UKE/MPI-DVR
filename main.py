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
        # speed slider and the play/pause button. A frame rate 
        # of 21.5ms can only be achieved using a very dedicated hardware setup
        self.t_ms = 21.5    
        
        # Dimension of vtk image data to be visualized. The source data 
        # will be interpolated to this size if variable "interpolation" is set to true,
        # otherwise original image dimensions of source will be used. Can be 
        # changed during visualization using the UI
        self.interpolation = False
        self.dims = [25, 25, 25]    
         
        # Create diagram class objects. Functions: 
        # - analyze image values of image series to find adequate
        #   visualization parameters for sliders
        # - draw image value histogram
        # - draw lookup table curve         
        self.diagram_op = plotDiagrams()  
        
        # Creation of vtk class object to invoke the buildup
        # of visualization pipeline
        self.vtk_op = vtk_pipeline()   
            
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
        interface.enableDisableButtons(self,False)        
        self.button_load_mdf_file.setEnabled(True)
        self.button_load_mha_files.setEnabled(True)
        self.button_saving_directory_screenshots.setEnabled(True)        
        
        # Set main window visible and access render window interactor
        self.show()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.vtk_op.iren = self.iren 
        self.vtk_op.vtk_widget = self.vtkWidget
        self.iren.Initialize()
        self.iren.Start()    
        
        # Create timer to constantly update VTK pipeline.
        # Timer can be paused / started via the QT pause / play button
        self.timer = Qt.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_status) 
        self.previous_time = time.time()
        
        # Create timer to constantly update the display of camera position 
        # and focal point on the visualization screen
        self.timer_cp = Qt.QTimer(self)
        self.timer_cp.setSingleShot(False)
        self.timer_cp.timeout.connect(self.displayPos) 
        self.timer_cp.start(1)
        
        
    def update_status(self): 
        """
        This function updates the VTK pipeline by feeding the 
        volume mapper object the subsequent image data object.
        It will be constantly invoked by the QT timer object. 
        The corresponding image data is aquired using the mdf / mha reader.         
        """        
        # Defines number of image that will be visualized
        self.count = self.count + 1 
        # Reset image count if out of boundary 
        # --> Image sequence restarts from the beginning 
        if self.count > self.number_of_total_images:
            self.count = 1             
  
        if self.source_data_format == 'mha':            
            self.temporary_image = create_VTK_data_from_mha_file(self.directory_source, self.count, self.interpolation, self.dims)
            
        if self.source_data_format == 'mdf':            
            self.temporary_image = create_VTK_data_from_HDF(self.directory_mdf, self.count-1, self.interpolation, self.dims)           
        
        self.vtk_op.volumeMapperBolus.SetInputData(self.temporary_image)        
        
        # Buildup of roadmap. Gets deactivated if whole cycle has been
        # completed
        if self.checkbox_roadmap_buildup.isChecked() and \
        self.roadmap_counter <= self.number_of_total_images:
            self.vtk_op.roadmap_buildup(self.temporary_image) 
            self.roadmap_counter = self.roadmap_counter+1
                
        # Computation of real frame rate        
        self.label_frame_rate_display.setText(str(round(1.0 / (time.time() - self.previous_time), 2)))
        self.previous_time = time.time()   
        
        # Update image count display
        image_count = str(self.count) + ' / ' + str(self.number_of_total_images)
        self.label_image_count_display.setText(str(image_count) )
        
        # Save screenshots of visualized MPI data if checked
        if self.checkbox_save_images.isChecked():
            interface.screenshot_and_save(self)  
            
        # Render image
        self.iren.Initialize()
        self.iren.Start()    
    
    def displayPos(self):  
        """ 
        This function is constantly invoked by timer_cp and thereby 
        continously updates the camera specifications (camera position, focal
        point)
        """
        pos = self.vtk_op.ren.GetActiveCamera().GetPosition()
        fp = self.vtk_op.ren.GetActiveCamera().GetFocalPoint()
        text = 'Camera: ' + str( round(pos[0], 1)) + ', ' + str( round(pos[1], 1)) + ', ' \
            + str( round(pos[2], 1)) + ' \nFocal point: ' + str( round(fp[0], 1)) + ', '  \
            + str( round(fp[1], 1)) + ', ' \
            + str( round(fp[2], 1))         
        self.vtk_op.text_actor.SetInput( text )


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())