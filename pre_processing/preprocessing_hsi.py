import rasterio
import numpy as np
from rasterio.enums import Resampling
import albumentations as A

IMAGE_PATH = ...

PATCH_HEIGHT = 128
PATCH_WIDTH = 128
STEP = 128    
#this is done in a seperate file, as the hsi data is too big
#hsi file is very large, so preprocessing it takes a lot of RAM and time
#the data was originally stored as integers and has to be converted to floats (which is very computationally expensive with 368 channels)

#scale a single patch to range [0,1]
def standardize_patch(dataset:np.array, mins, ranges):
    z = np.copy(dataset.astype(np.float32))
    for i,band in enumerate(z):
        
        band=band.astype(np.float32)
        band = np.divide(np.subtract(band,mins[i],casting='unsafe'),ranges[i],casting='unsafe')

        z[i] = band
    return z
  
def crop_and_save():
    #height and width of reference data, but HSI data has the same shape
    height = 4036
    width = 6232
    
    save_path = ...
    
    #min and (max-min) for each channel
    mins = []
    ranges = []
    
    with  rasterio.open(IMAGE_PATH + "HySpex.tif") as x:
        print('opened')
        hsi_image_array = x.read()
        print('np')
        print(hsi_image_array.shape)
     
    print('Opened HSI')
    for i,band in enumerate(hsi_image_array):
        min = np.min(band)
        max = np.max(band)
        mins.append(min)
        ranges.append(max - min) 
        print(i, mins[i],ranges[i]) 
    print(mins)
    print(ranges)

     
    left, top,current_id = 0,0,0
    #get the cropped patches
    while top + PATCH_HEIGHT < height:
        while left + PATCH_WIDTH < width:
            patch = standardize_patch(hsi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH],mins,ranges)
            print(np.mean(patch))
            np.save(save_path + "hsi_images\hsi" + str(current_id) + ".npy",patch)
            print(current_id)
            
            current_id +=1
            left += STEP

            
        left = width - PATCH_WIDTH
        
        patch = standardize_patch(hsi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH],mins,ranges)
        np.save(save_path + "hsi_images\hsi" + str(current_id) + ".npy",patch)
        current_id +=1
        top += STEP
        left = 0
        print("Current ID: " + str(current_id))
        print("Current top: " + str(top))
        
        
    top = height - PATCH_HEIGHT
    while left + PATCH_WIDTH < height:
            patch = standardize_patch(hsi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH],mins,ranges)
            np.save(save_path + "hsi_images\hsi" + str(current_id) + ".npy",patch)
            current_id +=1
            left += STEP
            
    left = width - PATCH_WIDTH
        
    patch = standardize_patch(hsi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH],mins,ranges)
    np.save(save_path + "hsi_images\hsi" + str(current_id) + ".npy",patch)
    
    
if __name__ == "__main__":
   crop_and_save()
