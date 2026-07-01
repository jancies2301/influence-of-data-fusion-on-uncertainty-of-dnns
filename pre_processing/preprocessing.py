import rasterio
import numpy as np
from rasterio.enums import Resampling

IMAGE_PATH = ...

PATCH_HEIGHT = 128
PATCH_WIDTH = 128
STEP = 128    
#scale a given modality to the range [0,1]
def standardize(dataset:np.array):
    z = np.copy(dataset.astype(np.float32))
    for i,band in enumerate(dataset):
        # x_1 = (x-min)/(max - min)
        min = np.min(band)
        max = np.max(band)
        print(min,max)
        z[i] = np.divide(np.subtract(band,min,casting='unsafe'),max-min,casting='unsafe')

    return z

#preprocess the data
def crop_and_save(path:str):
    
    save_path = ...
    mask = rasterio.open(IMAGE_PATH + "OSM_label\osm_landuse.tif")
    #other modalities are resampled to this shape
    width = mask.width
    height = mask.height
    mask = mask.read(1)
    
    print('Opened mask')

    with  rasterio.open(IMAGE_PATH + "Sentinel-2.tif") as x:
        msi_image_array = standardize(x.read(out_shape = (x.count,height,width), resampling = Resampling.bilinear))
    print('Opened multispectral')
    
    with  rasterio.open(IMAGE_PATH + "3K_DSM.tif") as x:
        dsm_image_array = standardize(x.read(out_shape = (x.count,height,width), resampling = Resampling.bilinear))
    print('Opened DSM')
      
    with  rasterio.open(IMAGE_PATH + "Sentinel-1.tif") as x:
        #sar data is first scaled to dB
        sar_image_array = standardize(10*np.log10(x.read(out_shape = (x.count,height,width), resampling = Resampling.bilinear)))
    print('Opened SAR')    
    
    with  rasterio.open(IMAGE_PATH + "3K_RGB.tif") as x:
        rgb_image_array = x.read(out_shape = (x.count,height,width), resampling = Resampling.bilinear)
    print('Opened RGB')
    
    #save whole images
    np.save(save_path + "msi_images\entire_city_msi"  + ".npy",msi_image_array)
    np.save(save_path + "masks\entire_city_mask"  + ".npy",mask)
    np.save(save_path + "sar_images\entire_city_sar"+ ".npy",sar_image_array)
    np.save(save_path + "rgb_images\entire_city_image" ".npy",rgb_image_array)
    np.save(save_path + "dsm_images\entire_city_dsm" + ".npy",dsm_image_array)
    left, top,current_id = 0,0,0
    
    #travererse the images and save 128x128 patches
    while top + PATCH_HEIGHT < height:
        while left + PATCH_WIDTH < width:
            np.save(save_path + "msi_images\msi" + str(current_id) + ".npy",msi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "masks\mask" + str(current_id) + ".npy",mask[top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "sar_images\sar" + str(current_id) + ".npy",sar_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "rgb_images\image" + str(current_id) + ".npy",rgb_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "dsm_images\dsm" + str(current_id) + ".npy",dsm_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            print(current_id)
            
            current_id +=1
            left += STEP
   
        left = width - PATCH_WIDTH
        
        np.save(save_path + "msi_images\msi" + str(current_id) + ".npy",msi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
        np.save(save_path + "masks\mask" + str(current_id) + ".npy",mask[top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
        np.save(save_path + "sar_images\sar" + str(current_id) + ".npy",sar_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
        np.save(save_path + "rgb_images\image" + str(current_id) + ".npy",rgb_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
        np.save(save_path + "dsm_images\dsm" + str(current_id) + ".npy",dsm_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
        current_id +=1
        top += STEP
        left = 0
        print("Current ID: " + str(current_id))
        print("Current top: " + str(top))
        
        
    top = height - PATCH_HEIGHT
    while left + PATCH_WIDTH < height:
            np.save(save_path + "msi_images\msi" + str(current_id) + ".npy",msi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "masks\mask" + str(current_id) + ".npy",mask[top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "sar_images\sar" + str(current_id) + ".npy",sar_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            np.save(save_path + "rgb_images\image" + str(current_id) + ".npy",rgb_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
            current_id +=1
            left += STEP
            
    left = width - PATCH_WIDTH
        
    np.save(save_path + "msi_images\msi" + str(current_id) + ".npy",msi_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
    np.save(save_path + "masks\mask" + str(current_id) + ".npy",mask[top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
    np.save(save_path + "sar_images\sar" + str(current_id) + ".npy",sar_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
    np.save(save_path + "rgb_images\image" + str(current_id) + ".npy",rgb_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
    np.save(save_path + "dsm_images\dsm" + str(current_id) + ".npy",dsm_image_array[:,top:top+PATCH_HEIGHT,left:left+PATCH_WIDTH])
if __name__ == "__main__":
    crop_and_save(IMAGE_PATH)
