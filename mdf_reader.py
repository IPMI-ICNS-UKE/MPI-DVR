# -*- coding: utf-8 -*-

import h5py
import vtk
import numpy as np

def create_VTK_data_from_HDF(directory_mdf, count, interpolation, vtk_image_data_dimensions):
    
    
    f = h5py.File(str(directory_mdf),'r')
    
    dset_size = f['reconstruction/size']
    dset_data = f['reconstruction/data'] 
    dset_FOV = f['reconstruction/fieldOfView']

    
    
    imageData = vtk.vtkImageData()
    imageData.SetDimensions(dset_size[0], dset_size[1], dset_size[2])
    imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)    
    imageData.SetSpacing(dset_FOV[0] / dset_size[0] * 1000.0, \
             dset_FOV[1] / dset_size[1] * 1000.0, dset_FOV[2] / dset_size[2] * 1000)


    data_array = np.array(dset_data[count,:,0])   
    
    counter = 0
    
    for z in range(dset_size[2]):
        for y in range(dset_size[1]):
            for x in range(dset_size[0]):
                imageData.SetScalarComponentFromDouble(x, y, z, 0, data_array[counter] )                
               
                counter = counter+1        
                
    
    if interpolation == True:
        resize = vtk.vtkImageResize()
        resize.SetInputData(imageData)
        resize.SetOutputDimensions(vtk_image_data_dimensions)
        resize.Update()
        imageData = resize.GetOutput()
    
    
    
    return imageData

def return_dimensions_image_data(directory_mdf):    
    return h5py.File(str(directory_mdf),'r')['reconstruction/size']

                
def get_number_of_images(directory_mdf):    
    
    f = h5py.File(str(directory_mdf),'r')    
    
    dset_data = f['reconstruction/data']
           
    return dset_data.shape[0]

def return_data_array(directory_mdf):
    f = h5py.File(str(directory_mdf),'r')
    return np.array(f['reconstruction/data'][:,:,0]).flatten()
