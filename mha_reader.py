# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""

import os.path
import vtk


def create_mha_file_name(directory_source, count):
    name_part1 = directory_source   
    name_part2 = "/%d.mha" %count  
    name = name_part1 + name_part2
    return name   
   
    

def create_VTK_data_from_mha_file(directory_source, count, interpolation, vtk_image_data_dimensions):
    name = create_mha_file_name(directory_source, count) 
    
    if os.path.isfile(name):
        imageReader = vtk.vtkMetaImageReader() 
        imageReader.SetFileName(name) 
        imageReader.Update()      
    
    if interpolation == True: 
        resize = vtk.vtkImageResize()
        resize.SetInputData(imageReader.GetOutput())
        resize.SetOutputDimensions(vtk_image_data_dimensions)
        resize.Update()
        imageData1 = resize.GetOutput()
    else:
        imageData1 = imageReader.GetOutput()        
  
    return imageData1
    

def get_number_of_image_data(directory_source): 
    counter = 1
    name = create_mha_file_name(directory_source, counter)
    image_data_exists = True
    while (image_data_exists):
        if os.path.isfile(name):
            counter = counter + 1
            name = create_mha_file_name(directory_source, counter)
            
        else:
            image_data_exists = False
    
    return counter - 1
        
       

    
    
        