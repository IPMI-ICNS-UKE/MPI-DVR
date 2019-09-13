# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""
 
# External libraries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# Own functions 
import mha_reader
import mdf_reader


class plotDiagrams:
    def __init__(self):
        self.figure = Figure()
        self.figure.set_size_inches(9, 5.5)
        self.canvas = FigureCanvas(self.figure)       
        self.ax = self.figure.add_subplot(211,yscale='log')    
        self.ax.set_ylabel("Count", fontsize=16, color="grey")        
        self.ax2 = self.figure.add_subplot(212)     
        self.ax2.set_ylabel("Opacity", fontsize=16, color="grey")
        self.ax2.set_xlabel("Image value", fontsize=16, color="grey")
        self.canvas.draw()     
        self.data_bin = []
        self.opacity_max_bolus = 0.5
        self.opacity_max_roadmap = 0.5
        self.threshold_bolus = 20.0
        self.threshold_roadmap = 20.0
        self.intervall_bolus = 100.0
        self.intervall_roadmap = 100.0
        self.image_analysis_step_size = 5
        self.down_sample_size = [25, 25, 25]
        self.max_image_value  = 100.0
        self.min_image_value = 0.0
        self.color_bolus = 'red'
        self.color_roadmap = 'green'        
        self.manual_lookup_table_matrix = None        
        self.number_of_ramp_points = 10.0        
        self.manual_lookup_table_bolus = False
        self.manual_lookup_table_roadmap = False
        self.manual_lookup_table_matrix_bolus = []
        self.manual_lookup_table_matrix_roadmap = []

    def drawHistogram(self):                
        self.ax.clear()
        self.ax.set_xlim( min(self.data_bin), max(self.data_bin)  )
        self.ax.set_yscale('log')        
        self.ax.hist(self.data_bin, bins=40)         
        self.ax.plot()    
        self.canvas.draw()            
            
    def computeHistogramDataBin(self, directory, mode):    
        """
        This function gathers image values of the dataset in order 
        to create a data bin that is used for histogram visualization. 
        """       
        self.data_bin = []         
        if mode == 'mdf':                        
            self.data_bin = mdf_reader.return_data_array(directory)             
        if mode == 'mha':  
            self.data_bin = mha_reader.return_data_array(directory)            
        self.max_image_value  = max(self.data_bin)
        self.min_image_value = min(self.data_bin)
        self.total_image_value_range = self.max_image_value - self.min_image_value        
        self.threshold_bolus =  self.total_image_value_range / 2.0
        self.threshold_roadmap = self.total_image_value_range / 2.0
        self.intervall_bolus = self.total_image_value_range / 2.0
        self.intervall_roadmap = self.total_image_value_range / 2.0
    
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
    
    def computeRampPoints(self, variable_ending):
        opacity_max_string = 'self.opacity_max_' + variable_ending        
        opacity_max = eval(opacity_max_string)        
        intervall_string = 'self.intervall_' + variable_ending 
        intervall = eval(intervall_string)        
        threshold_string = 'self.threshold_' + variable_ending 
        threshold = eval(threshold_string)    
        
        x_increment = intervall / self.number_of_ramp_points
        x_start = threshold
        x_end = threshold + intervall + 0.5 * x_increment        
        x_range = np.arange(x_start, x_end, x_increment)        
        opacity_values = self.linearRampFunction(variable_ending, x_range)
        # Append plateau of Lookup curve to diagram
        x_range = np.append(x_range, 2 * self.max_image_value)
        opacity_values = np.append(opacity_values, opacity_max)                  
        return x_range, opacity_values

        
        
    def drawLookupTable(self):
        """
        This function draws the curves representing bolus / roadmap lookup 
        table in ax2 diagram based on the variables: 
            - threshold_bolus, threshold_roadmap
            - intervall_bolus, intervall_roadmap
            - opacity_max_bolus, opacity_max_roadmap        
        In this version a linear ramp is used!
        """        
        self.ax2.clear()
        self.ax2.set_xlim(self.min_image_value , self.max_image_value )
        self.ax2.set_ylim(0, 1)        
        if self.manual_lookup_table_bolus == True:
            x = [row[0] for row in self.manual_lookup_table_matrix_bolus]
            y = [row[1] for row in self.manual_lookup_table_matrix_bolus]               
            new_x, new_y = zip(*sorted(zip(x, y)))             
            new_x = new_x + (2 * self.max_image_value,)
            new_x = (self.min_image_value - abs(self.min_image_value),) + new_x                
            new_y = new_y + (new_y[len(x)-1],)
            new_y = (new_y[0],) + new_y             
            p1 = (new_x, new_y)
        else: 
            p1 = self.computeRampPoints('bolus')
            
        if self.manual_lookup_table_roadmap == True:
            x = [row[0] for row in self.manual_lookup_table_matrix_roadmap]
            y = [row[1] for row in self.manual_lookup_table_matrix_roadmap]               
            new_x, new_y = zip(*sorted(zip(x, y)))            
            new_x = new_x + (2 * self.max_image_value,)
            new_x = (self.min_image_value - abs(self.min_image_value),) + new_x             
            new_y = new_y + (new_y[len(x)-1],)
            new_y = (new_y[0],) + new_y             
            p2 = (new_x, new_y)            
        else:             
            p2 = self.computeRampPoints('roadmap')
            
        # Draw lookup table curve bolus visualization
        self.ax2.plot(p1[0], p1[1], color=self.color_bolus)
        self.ax2.plot(p2[0], p2[1], color=self.color_roadmap)
        self.canvas.draw()
        

 

        

    
    
        