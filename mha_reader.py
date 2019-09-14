# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:23:58 2018

@author: domdo
"""

import os.path
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import random


def createMHAFileName(directory, count):
    name_part1 = directory   
    name_part2 = "/%d.mha" %count  
    name = name_part1 + name_part2
    return name   
   
def returnDimsFirstImage(directory):
    imageReader = vtk.vtkMetaImageReader() 
    imageReader.SetFileName(createMHAFileName(directory, 1)) 
    imageReader.Update()
    return imageReader.GetOutput().GetDimensions()

def returnSpacingFirstImage(directory):
    imageReader = vtk.vtkMetaImageReader() 
    imageReader.SetFileName(createMHAFileName(directory, 1)) 
    imageReader.Update()
    return imageReader.GetOutput().GetSpacing()
    
    

def createVTKDataFromMHAFile(directory, count, interpolation, vtk_image_data_dimensions):
    name = createMHAFileName(directory, count) 
    
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
    

def getNumberImages(directory): 
    counter = 1
    name = createMHAFileName(directory, counter)
    image_data_exists = True
    while (image_data_exists):
        if os.path.isfile(name):
            counter = counter + 1
            name = createMHAFileName(directory, counter)
            
        else:
            image_data_exists = False
    
    return counter - 1

def return_matrix_image(image_name):
    imr = vtk.vtkMetaImageReader()
    imr.SetFileName(image_name)
    imr.Update()
    
    im = imr.GetOutput()        
    sc = im.GetPointData().GetScalars()
    a =  vtk_to_numpy(sc)        
    print (a.shape)
    return a

def return_total_data_bin(directory):
    count = 1
    name = createMHAFileName(directory, count) 
    data_bin = np.array([])
    while( os.path.isfile(name)):         
        data_bin = np.append(data_bin,return_matrix_image(name))
        count = count + 1        
        name = createMHAFileName(directory, count)  
    
    return data_bin

def computeMinMax(directory):
    count = 1
    name = createMHAFileName(directory, 1) 
    min_ = np.amin(return_matrix_image(name))
    max_ = np.amax(return_matrix_image(name))
    while( os.path.isfile(name)):         
        if min_ < np.amin(return_matrix_image(name)):
            min_ = np.amin(return_matrix_image(name))
        if max_ < np.amax(return_matrix_image(name)):
            max_ = np.amax(return_matrix_image(name))
            
        count = count + 1        
        name = createMHAFileName(directory, count)          
    print("Min/Max:", min_, max_)
    return [min_, max_]
    

def returnDataArray(directory, bool_create_histo, only_max_min, less_images):
    data_bin = np.array([])
    total_number_images = getNumberImages(directory)
    if less_images is not None and total_number_images > less_images:
        idx = random.sample(range(total_number_images), less_images)
        idx_ = np.sort(idx)  
        for i in idx_:
            print ("  ",i)
            name = createMHAFileName(directory, i) 
            data_bin = np.append(data_bin, return_matrix_image(name))
    
    else: 
        if bool_create_histo == True:                
                data_bin = return_total_data_bin(directory)
        else: 
            if only_max_min == True:                
                data_bin = np.array(computeMinMax(directory))
            else: 
                data_bin = np.zeros(2)   
    
    return data_bin
    

        
       

    
    
        