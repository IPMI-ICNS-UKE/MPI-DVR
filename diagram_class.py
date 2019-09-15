"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""
 
# External libraries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


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
        self.op_max_bl = None
        self.op_max_rm = None
        self.th_bl = None
        self.th_rm = None
        self.ri_bl = None
        self.ri_rm = None
        self.image_analysis_step_size = 5
        self.down_sample_size = [25, 25, 25]
        self.max_value  = 0.1
        self.min_value = 0.0
        self.color_bl = 'red'
        self.color_rm = 'green'        
        self.manual_lookup_table_matrix = None        
        self.number_of_ramp_points = 10.0        
        self.manual_lookup_table_bl = False
        self.manual_lookup_table_rm = False
        self.manual_lookup_table_matrix_bl = []
        self.manual_lookup_table_matrix_rm = []
        
        self.less_images = None
        self.bool_create_histogram = True
        self.bool_max_min = True

    def drawHistogram(self):   
        if self.bool_create_histogram == True:             
            self.ax.clear()
            self.ax.set_xlim( min(self.data_bin), max(self.data_bin)  )
            self.ax.set_yscale('log')        
            self.ax.hist(self.data_bin, bins=40)   
            self.ax.plot()    
            self.canvas.draw()  
            
        else: 
            self.ax.clear()         
            # Draw text into diagram: Histogram analysis disabled
            self.ax.text(0.5, 0.7, "Disabled", size=50,transform=self.ax.transAxes, ha="right", va="top",\
                         bbox=dict(boxstyle="square", ec=(1., 0.5, 0.5), \
                                   fc=(1., 0.8, 0.8), ) )
            
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
    
    def computeRampPoints(self, variable_ending):
        op_max_string = 'self.op_max_' + variable_ending        
        op_max = eval(op_max_string)        
        ri_string = 'self.ri_' + variable_ending 
        ri = eval(ri_string)        
        th_string = 'self.th_' + variable_ending 
        th = eval(th_string)    
       
        
        
        x_increment = ri / self.number_of_ramp_points
        x_start = th
        x_end = th + ri + 0.5 * x_increment        
        x_range = np.arange(x_start, x_end, x_increment)        
        op_values = self.linearRampFunction(variable_ending, x_range)
        # Append plateau of Lookup curve to diagram
        x_range = np.append(x_range, 2 * self.max_value)
        op_values = np.append(op_values, op_max)                  
        return x_range, op_values

        
        
    def drawLookupTable(self):
        """
        This function draws the curves representing bl / rm lookup 
        table in ax2 diagram based on the variables: 
            - th_bl, th_rm
            - ri_bl, ri_rm
            - op_max_bl, op_max_rm        
        In this version a linear ramp is used!
        """        
        self.ax2.clear()
        self.ax2.set_xlim(self.min_value , self.max_value )
        self.ax2.set_ylim(0, 1)        
        if self.manual_lookup_table_bl == True:
            x = [row[0] for row in self.manual_lookup_table_matrix_bl]
            y = [row[1] for row in self.manual_lookup_table_matrix_bl]               
            new_x, new_y = zip(*sorted(zip(x, y)))             
            new_x = new_x + (2 * self.max_value,)
            new_x = (self.min_value - abs(self.min_value),) + new_x                
            new_y = new_y + (new_y[len(x)-1],)
            new_y = (new_y[0],) + new_y             
            p1 = (new_x, new_y)
        else: 
            p1 = self.computeRampPoints('bl')
            
        if self.manual_lookup_table_rm == True:
            x = [row[0] for row in self.manual_lookup_table_matrix_rm]
            y = [row[1] for row in self.manual_lookup_table_matrix_rm]               
            new_x, new_y = zip(*sorted(zip(x, y)))            
            new_x = new_x + (2 * self.max_value,)
            new_x = (self.min_value - abs(self.min_value),) + new_x             
            new_y = new_y + (new_y[len(x)-1],)
            new_y = (new_y[0],) + new_y             
            p2 = (new_x, new_y)            
        else:             
            p2 = self.computeRampPoints('rm')
            
        # Draw lookup table curve bl visualization
        self.ax2.plot(p1[0], p1[1], color=self.color_bl)
        self.ax2.plot(p2[0], p2[1], color=self.color_rm)
        self.canvas.draw()
        

 

        

    
    
        