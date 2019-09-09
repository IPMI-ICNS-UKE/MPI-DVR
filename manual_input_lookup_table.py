# External libraries
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import Qt

 
class TableView(Qt.QMainWindow):
    def __init__(self, parent, mode, lookup_table, *args):
        super(TableView, self).__init__(parent)         
        
        self.currentData = mode        
        self.image_values = [0, 1]
        self.opacity_values = [0, 1]
        self.lookup_table_matrix = list(zip(self.image_values, self.opacity_values))
             
        # Creation of table, count of rows and columns in *args
        self.table1 = QTableWidget( *args)
        self.table1.setHorizontalHeaderLabels(['Image value','Opacity'])
        self.table1.resizeColumnsToContents()
        self.table1.resizeRowsToContents()        
        self.table1.itemChanged.connect(self.item_changed)   
        
        if (lookup_table != None):
            self.lookup_table_matrix = lookup_table
            self.buildupLookupTableFromLookmatrix()  
        
        
        # Initiation of button widgets and box layout  
        self.button_update_lookup_table = Qt.QPushButton('Update lookup table')
        self.button_update_lookup_table.clicked.connect(self.adaptCurrentLookupTable)
        
        self.button_remove_row = Qt.QPushButton('Remove entry')
        self.button_remove_row.clicked.connect(self.removeRow)
        
        self.button_add_row = Qt.QPushButton('Add entry')
        self.button_add_row.clicked.connect(self.addRow)
        
        self.label_table = Qt.QLabel()
        self.label_table.setText('Lookup table ' + mode)
        
        self.frame = Qt.QFrame()  
        self.vl = Qt.QVBoxLayout()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        
        self.hl_buttons = Qt.QHBoxLayout()      
        self.hl_buttons.addWidget(self.button_update_lookup_table)
        self.hl_buttons.addWidget(self.button_add_row)
        self.hl_buttons.addWidget(self.button_remove_row)       
        
        self.vl.addWidget(self.label_table)
        self.vl.addWidget(self.table1)
        self.vl.addLayout(self.hl_buttons)       
        
        self.show()
        
    def adaptCurrentLookupTable(self):
        temp_lst = []
        for i in range(self.table1.rowCount()):
            if (self.table1.item (i, 0) is not None and \
                self.table1.item (i, 1) is not None):
                
                a = float(self.table1.item (i, 0).text())    
                b = float(self.table1.item (i, 1).text()) 
                temp_lst.append([a,b])
        
        if self.currentData == 'bolus':            
            self.parent().manual_lookup_table_bolus = temp_lst
            self.parent().diagram_op.manual_lookup_table_bolus = True
            self.parent().diagram_op.manual_lookup_table_matrix_bolus = temp_lst
            self.parent().diagram_op.drawLookupTable()
            self.parent().vtk_op.lookup_table_matrix = temp_lst
            a = self.parent().vtk_op.create_lookup_table_from_manual_input()
            self.parent().vtk_op.volumePropertyBolus.SetScalarOpacity(a)
            
        if self.currentData == 'roadmap':
            self.parent().manual_lookup_table_roadmap = temp_lst
            self.parent().diagram_op.manual_lookup_table_roadmap = True
            self.parent().diagram_op.manual_lookup_table_matrix_roadmap = temp_lst
            self.parent().diagram_op.drawLookupTable()
            self.parent().vtk_op.lookup_table_matrix = temp_lst
            a = self.parent().vtk_op.create_lookup_table_from_manual_input()
            self.parent().vtk_op.volumePropertyRoadmap.SetScalarOpacity(a)
            
        self.parent().iren.Initialize()
        self.parent().iren.Start()
        self.lookup_table_matrix = temp_lst
            

        
    def buildupLookupTableFromLookmatrix(self):

        for i in range(len([row[0] for row in self.lookup_table_matrix])):
            
            newitem = QTableWidgetItem(str(self.lookup_table_matrix[i][0]))
            newitem2 = QTableWidgetItem(str(self.lookup_table_matrix[i][1]))
            self.table1.setItem(i, 0, newitem)
            self.table1.setItem(i, 1, newitem2)
        
    
       

    def item_changed(self, Qitem):        
        try:
            test = float(Qitem.text())
        except ValueError:
            Msgbox = Qt.QMessageBox()
            Msgbox.setText("Value must be number! Use '.' for decimal places!")
            Msgbox.exec()
            Qitem.setText(str(self.lookup_table_matrix[Qitem.row()][Qitem.column()]))

        
        
    def addRow(self):
        rowPosition = self.table1.rowCount()
        self.table1.insertRow(rowPosition)
        
        self.table1.resizeColumnsToContents()
        self.table1.resizeRowsToContents()
        
    def removeRow(self, Qitem):
        rowPosition = self.table1.rowCount()-1
        self.table1.removeRow(rowPosition)
 
        self.table1.resizeColumnsToContents()
        self.table1.resizeRowsToContents()
