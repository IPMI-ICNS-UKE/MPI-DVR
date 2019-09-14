# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:07:58 2018

@author: domdo
"""

import sys
from PyQt5 import Qt
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import mdf_reader 
import mha_reader 
import diagram_class
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
        self.diagram_op = diagram_class.plotDiagrams()  
        
        # Creation of vtk class object to invoke the buildup
        # of visualization pipeline
        self.vtk_op = vtk_pipeline()   
            
        # Create QT display interfaces that show visualization pipeline óutput             
        self.frame = Qt.QFrame()      
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)        
        self.setCentralWidget(self.frame)        

        # Defintion of standard min/max image values and the  starting 
        # positions of the sliders (sl = slider, pos = position, 
        # bl = bl, rm = roadmap, op = op, st = steepness ramp, 
        # th = th). Those values will be used if pre image analysis 
        # is deactivated.
        self.min_value = 0.0
        self.max_value = 0.1
        
        self.sl_pos_th_bl = 0.5
        self.sl_pos_th_rm = 0.5
        
        self.sl_pos_op_bl = 0.5
        self.sl_pos_op_rm = 0.5   
        
        self.sl_pos_ri_bl = 0.5
        self.sl_pos_ri_rm = 0.5        
        
        self.updateVisualizationParameters()


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
        self.combobox_pre_image_analysis.setEnabled(True) 
        
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
        self.timer.timeout.connect(self.updateStatus) 
        self.previous_time = time.time()
        
        # Create timer to constantly update the display of camera position 
        # and focal point on the visualization screen
        self.timer_cp = Qt.QTimer(self)
        self.timer_cp.setSingleShot(False)
        self.timer_cp.timeout.connect(self.displayPos) 
        self.timer_cp.start(1)
        
        # Defintion of directory variables
        self.directory_output = None
        self.directory_mha = None
        self.directory_mdf = None
        

        
    def updateStatus(self): 
        """
        This function updates the VTK pipeline by feeding the 
        volume mapper object the subsequent image data object.
        It will be constantly invoked by the QT timer object. 
        The corresponding image data is aquired using the mdf / mha reader.         
        """        
        # Defines number of image that will be visualized
        self.image_count = self.image_count + 1 
        # Reset image count if out of boundary 
        # --> Image sequence restarts from the beginning 
        if self.image_count > self.number_of_total_images:
            self.image_count = 1             
  
        if self.source_data_format == 'mha':            
            self.temporary_image = mha_reader.createVTKDataFromMHAFile(self.directory_mha, self.image_count, self.interpolation, self.dims)
            
        if self.source_data_format == 'mdf':            
            self.temporary_image = mdf_reader.createVTKDataFromHDF(self.directory_mdf, self.image_count-1, self.interpolation, self.dims)           
        
        self.vtk_op.volumeMapperbl.SetInputData(self.temporary_image)        
        
        # Buildup of roadmap. Gets deactivated if whole cycle has been
        # completed
        if self.checkbox_rm_buildup.isChecked() and \
        self.rm_counter <= self.number_of_total_images:
            self.vtk_op.rmBuildup(self.temporary_image) 
            self.rm_counter = self.rm_counter+1
                
        # Computation of real frame rate        
        self.label_frame_rate_display.setText(str(round(1.0 / (time.time() - self.previous_time), 2)))
        self.previous_time = time.time()   
        
        # Update image count display
        image_count = str(self.image_count) + ' / ' + str(self.number_of_total_images)
        self.label_image_count_display.setText(str(image_count) )
        
        # Save screenshots of visualized MPI data if checked
        if self.checkbox_save_images.isChecked():
            interface.screenshotAndSave(self)  
            
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
    
    def updateVisualizationParameters(self):
        # Compute visualization parameters 
        diff = self.max_value - self.min_value        
        self.op_max_bl = self.vtk_op.op_max_bl = self.diagram_op.op_max_bl = \
            self.sl_pos_th_bl
        self.op_max_rm = self.vtk_op.op_max_rm = self.diagram_op.op_max_rm = \
            self.sl_pos_th_rm
        
        self.th_bl = self.vtk_op.th_bl = self.diagram_op.th_bl = \
            self.min_value + diff * self.sl_pos_th_bl
        self.th_rm = self.vtk_op.th_rm = self.diagram_op.th_rm = \
            self.min_value + diff * self.sl_pos_th_rm
            
        self.ri_bl = self.vtk_op.ri_bl = self.diagram_op.ri_bl = \
            diff * self.sl_pos_ri_bl
        self.ri_rm = self.vtk_op.ri_rm = self.diagram_op.ri_rm = \
            diff * self.sl_pos_ri_rm
            
        self.vtk_op.min_value = self.diagram_op.min_value = self.min_value
        self.vtk_op.max_value = self.diagram_op.max_value = self.max_value

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())