# External libraries
from PyQt5 import Qt

 
class ColorMapSettingsView(Qt.QMainWindow):
    def __init__(self, parent, mode):
        super(ColorMapSettingsView, self).__init__(parent)         
        
        self.max_value = 100.0
        self.min_value = 0.0                         
        self.currentData = mode       
        
        # Initiation of button / lineedit / label widgets  
        self.button_update_lookup_table = Qt.QPushButton('Activate color map')
        self.button_update_lookup_table.clicked.connect(self.adaptColormapMinMax)
        
        self.label_min_value = Qt.QLabel(self)
        self.label_min_value.setText('Min value (yellow):' )
        self.label_min_value.setFixedWidth(125)        
        
        self.label_max_value = Qt.QLabel(self)
        self.label_max_value.setText('Max value (red):' )
        self.label_max_value.setFixedWidth(125) 
        
        self.lineedit_min_value = Qt.QLineEdit(self)
        self.lineedit_min_value.setText(str(self.min_value))
        
        self.lineedit_max_value = Qt.QLineEdit(self)
        self.lineedit_max_value.setText(str(self.max_value))
        
        self.checkbox_scalar_bar = Qt.QCheckBox("Show scalar bar", self)
        self.checkbox_scalar_bar.setChecked(False)
        self.checkbox_scalar_bar.stateChanged.connect(self.functionCheckboxScalarBar)
        
        # Boxlayout 
        self.frame = Qt.QFrame()  
        self.vl = Qt.QVBoxLayout()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)        
        self.hl_min_value = Qt.QHBoxLayout()      
        self.hl_min_value.addWidget(self.label_min_value)
        self.hl_min_value.addWidget(self.lineedit_min_value)        
        self.hl_max_value = Qt.QHBoxLayout()      
        self.hl_max_value.addWidget(self.label_max_value)
        self.hl_max_value.addWidget(self.lineedit_max_value)        
        self.vl.addLayout(self.hl_min_value)
        self.vl.addLayout(self.hl_max_value)
        self.vl.addWidget(self.checkbox_scalar_bar)
        self.vl.addWidget(self.button_update_lookup_table)       
        
     
        
    def adaptColormapMinMax(self):
        try:         
            le_min_input = float(self.lineedit_min_value.text())        
            le_max_input = float(self.lineedit_max_value.text())        
            self.max_value = le_max_input
            self.min_value = le_min_input        
            self.parent().vtk_op.updateColorMap(self.currentData, le_min_input, le_max_input)
            self.functionCheckboxScalarBar()
        except: 
            print("Enter valid values!")
    
    def functionCheckboxScalarBar(self):
        """ 
        This function is used to show / hide scalar bar on the visualization 
        screen 
        """        
        if not self.checkbox_scalar_bar.isChecked():    
            if self.currentData == 'bl':                          
                self.parent().vtk_op.ren.RemoveActor2D(self.parent().vtk_op.actor_scalar_bar_bl)
                if self.parent().vtk_op.bool_scalar_bar_rm == True:
                    self.parent().vtk_op.actor_scalar_bar_rm.SetPosition(0.03, 0.12)
                self.parent().vtk_op.bool_scalar_bar_bl = False
            if self.currentData == 'rm':                          
                self.parent().vtk_op.ren.RemoveActor2D(self.parent().vtk_op.actor_scalar_bar_rm)
                self.parent().vtk_op.bool_scalar_bar_rm = False
                if self.parent().vtk_op.bool_scalar_bar_bl == True:
                    self.parent().vtk_op.actor_scalar_bar_bl.SetPosition(0.03, 0.12)
            self.parent().iren.Initialize()
            self.parent().iren.Start()
        else:
            if self.currentData == 'bl':                          
                self.parent().vtk_op.bool_scalar_bar_bl = True
            if self.currentData == 'rm':                            
                self.parent().vtk_op.bool_scalar_bar_rm = True
            self.parent().vtk_op.updateScalarBar(self.currentData, self.min_value, self.max_value) 
            self.parent().iren.Initialize()
            self.parent().iren.Start()  
            
            
            
       
class InputColorRGB(Qt.QMainWindow):
    def __init__(self, parent, mode):
        super(InputColorRGB, self).__init__(parent)         
        self.currentData = mode   

        self.lineedit_RGB = Qt.QLineEdit(self)
        self.lineedit_RGB.setPlaceholderText('R, G, B (Value range: 0 .. 1)')
        
        self.button_update_rgb_color = Qt.QPushButton('Update')
        self.button_update_rgb_color.clicked.connect(self.adaptRGBColor)
        
        self.frame = Qt.QFrame()  
        self.vl = Qt.QVBoxLayout()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)   
        self.vl.addWidget(self.lineedit_RGB)
        self.vl.addWidget(self.button_update_rgb_color)    
                

    def adaptRGBColor(self):
        rgb_values = self.lineedit_RGB.text()
        print(rgb_values)
        rgb_values_ = rgb_values.split(",")  
        try:           
            r = float(rgb_values_[0])
            g = float(rgb_values_[1])
            b = float(rgb_values_[2])                   
            self.parent().vtk_op.setMonoColor(self.currentData, r, g, b)  
        except: 
            print("Enter valid values!")
        
        
        

