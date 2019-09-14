# -*- coding: utf-8 -*-

import h5py
import vtk
import numpy as np
import random 

def createVTKDataFromHDF(directory_mdf, count, interpolation, vtk_image_data_dimensions):
    f = h5py.File(str(directory_mdf),'r')    
    dset_size = f['reconstruction/size']
    dset_data = f['reconstruction/data'] 
    dset_FOV = f['reconstruction/fieldOfView']
   
    imageData = vtk.vtkImageData()
    imageData.SetDimensions(dset_size[0], dset_size[1], dset_size[2])
    imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)    
    imageData.SetSpacing(dset_FOV[0] / dset_size[0] * 1000, \
             dset_FOV[1] / dset_size[1] * 1000, dset_FOV[2] / dset_size[2] *1000)

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

def returnDimensionsImageData(directory_mdf):    
    return h5py.File(str(directory_mdf),'r')['reconstruction/size']

def returnSpacingImageData(directory_mdf):   
    dset_size = h5py.File(str(directory_mdf),'r')['reconstruction/size']
    dset_FOV =  h5py.File(str(directory_mdf),'r')['reconstruction/fieldOfView']
    spacing = [dset_FOV[0] / dset_size[0] * 1000, \
               dset_FOV[1] / dset_size[1] * 1000, 
               dset_FOV[2] / dset_size[2] *1000 ]
    print("Spacing: ", spacing)
    # NOTE: basic length unit had to be decreased, since VTK doesnt work with 
    # spacing < 0.1
    
    return spacing

                
def getNumberImages(directory_mdf):       
    f = h5py.File(str(directory_mdf),'r')      
    dset_data = f['reconstruction/data']           
    return dset_data.shape[0]

def returnDataArray(directory_mdf, bool_create_histo, only_max_min, less_images):
    """
    returnDataArray(directory, \
            self.boolCreateHistogram, self.getMaxMin, self.less_images)
    """
    f = h5py.File(str(directory_mdf),'r')
    
    if less_images is not None:
        total_number_images = getNumberImages(directory_mdf)
        if total_number_images < less_images:            
            data_bin = np.array(f['reconstruction/data'][:,:,0]).flatten()
            
        #idx = np.random.randint(total_number_images, size=less_images)
        
        #idx = np.sort(idx)
        
        idx = random.sample(range(total_number_images), less_images)
        idx_ = np.sort(idx)  
        print(idx_)
        data_bin = np.array(f['reconstruction/data'][idx_,:,0]).flatten()
        print('Shape: ', data_bin.shape)
    else:     
        if bool_create_histo == True:                
                data_bin = np.array(f['reconstruction/data'][:,:,0]).flatten()
        else: 
            if only_max_min == True:                
                value_min = np.amax(np.array(f['reconstruction/data'][:,:,0]).flatten())
                value_max = np.amin(np.array(f['reconstruction/data'][:,:,0]).flatten())
                data_bin = np.array([value_min, value_max])
            else: 
                data_bin = np.zeros(2)
            
    return data_bin
            
    

