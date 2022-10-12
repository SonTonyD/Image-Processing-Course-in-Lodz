from PIL import Image
import numpy as np
import click
import math

@click.group()
def ImageProcessing():
    pass

@ImageProcessing.command()
@click.option('--name', default="./Images/lenac.bmp", help='path of the image. Example:--name="./Images/lenac.bmp"  ')
@click.option('--brightness', default=0, help='Set the brightness intensity: positive number to increase it and negative to decrease.')
@click.option('--contrast', default=1.0, help='Set the contrast intensity: Can only take positive number. contrast<1 to decrease and contrast >1 to increase')
@click.option('--negative', default=-1.0, help='Set the negative intensity: Can only take positive number. negative<1 to decrease and negative >1 to increase')
def Elementary(name, brightness, contrast, negative):
    img = Image.open(name)
    image_matrix = np.array(img)
    
    #Parameters of the function
    dir_coeff = contrast * (-negative)
    origin_coeff = brightness + 128*(1-dir_coeff)
    
    #Check if it is a colored image or not
    if len(image_matrix.shape) == 3:
        #For colored images
        width, height, channel = image_matrix.shape
        for i in range(width):
            for j in range(height):
                for k in range(channel):
                    tmp = (dir_coeff * image_matrix[i,j,k]) + origin_coeff
                    if tmp >= 255:
                        image_matrix[i,j,k] = 255
                    elif tmp <= 0:
                        image_matrix[i,j,k] =  0
                    else:
                        image_matrix[i,j,k] = tmp
    else :
        #For gray scale images
        width, height = image_matrix.shape
        for i in range(width):
            for j in range(height):
                tmp = (dir_coeff * image_matrix[i,j]) + origin_coeff
                if tmp >= 255:
                    image_matrix[i,j] = 255
                elif tmp <= 0:
                    image_matrix[i,j] =  0
                else:
                    image_matrix[i,j] = tmp
    Image.fromarray(image_matrix).save("./Results/ElementaryOperation_result.bmp")


@ImageProcessing.command()
@click.option('--name', default="./Images/lenac.bmp", help='path of the image. Example:--name="./Images/lenac.bmp"  ')
@click.option('--hflip', default=False, help='Can be true or false. Flip the selected image horizontally')
@click.option('--vflip', default=False, help='Can be true or false. Flip the selected image vertically')
@click.option('--dflip', default=False, help='Can be true or false. Flip the selected image diagonally')
@click.option('--shrink', default=1, help='Example: 2 to shrink the image resolution by 2')
@click.option('--enlarge', default=1, help='Example: 2 to enlarge the image resolution by 2')
def Geometric(name, hflip, vflip, dflip, shrink, enlarge):
    img = Image.open(name)
    image_matrix = np.array(img)
    tmp = np.array(img)
    
    
    
    width = image_matrix.shape[0]
    height = image_matrix.shape[1]
    
    if shrink != 1 or enlarge != 1:
        width = round((image_matrix.shape[0]/shrink)*enlarge)
        height = round((image_matrix.shape[1]/shrink)*enlarge)
        emptyImage = np.array(Image.new('RGB', (round(width), round(height)), color = 'white'))
        tmp = emptyImage
    
    
    
    #Set Parameters according to the chosen option 
    iParamA, iParamB, jParamA, jParamB = (0, 1, 0, 1)
    if hflip:
        jParamA, jParamB = (height-1, -1)
    if vflip:
        iParamA, iParamB = (width-1, -1)
    if dflip:
        iParamA, iParamB, jParamA, jParamB = (width-1, -1, height-1, -1)
        
    #Check if it is a colored image or not 
    if len(image_matrix.shape) == 3:
        for i in range(width):
            for j in range(height):
                for k in range(3):
                    tmp[i,j,k] = image_matrix[math.floor(((iParamA+iParamB*i)*shrink)/enlarge), math.floor(((jParamA+jParamB*j)*shrink)/enlarge) ,k]          
    else:
        for i in range(width):
            for j in range(height):
                tmp[i,j] = image_matrix[math.floor(((iParamA+iParamB*i)*shrink)/enlarge), math.floor(((jParamA+jParamB*j)*shrink)/enlarge) ,k]  
    image_matrix = tmp
    Image.fromarray(image_matrix).save("./Results/GeometricOperation_result.bmp")


@ImageProcessing.command()
@click.option('--name', default="./Images/lenac.bmp", help='path of the image. Example:--name="./Images/lenac.bmp"  ')
@click.option('--mid', default=0, help='Use Midpoint filter: ex: 1 is one pixel around the current pixel (3x3)')
@click.option('--amean', default=0, help='Use Arithmetic mean filter: ex: 1 is one pixel around the current pixel (3x3)')
def Noise(name, mid, amean) :
    img = Image.open(name)
    image_matrix = np.array(img)
    tmp = np.array(img)
    
    width = image_matrix.shape[0]
    height = image_matrix.shape[1]
    
    #Set Parameters according to the chosen option 
    if mid != 0 :
        index_start = mid
    if amean != 0:
        index_start = amean
    
    
    if len(image_matrix.shape) == 3:
        for i in range(index_start,width-index_start):
            for j in range(index_start,height-index_start):
                for k in range(3):
                    max = -1
                    min = 257
                    avg = 0
                    for x in range(-index_start,index_start):
                        for y in range(-index_start,index_start):
                            current_pixel = image_matrix[i+x,j+y,k]
                            if mid != 0:
                                if max < current_pixel:
                                    max = current_pixel
                                if min > current_pixel:
                                    min = current_pixel
                            if amean != 0:
                                avg += current_pixel
                    if mid != 0:            
                        tmp[i,j,k] = (int(max) + int(min))/2
                    if amean != 0:
                        tmp[i,j,k] = avg/((2*amean+1)*(2*amean+1))
    else:
        for i in range(width):
            for j in range(height):
                max = -1
                min = 257
                avg = 0
                for x in range(-index_start,index_start):
                    for y in range(-index_start,index_start):
                        current_pixel = image_matrix[i+x,j+y]
                        if mid != 0:
                            if max < current_pixel:
                                max = current_pixel
                            if min > current_pixel:
                                min = current_pixel
                        if amean != 0:
                            avg += current_pixel
                if mid != 0:            
                    tmp[i,j] = (int(max) + int(min))/2
                if amean != 0:
                    tmp[i,j] = avg/((2*amean+1)*(2*amean+1))
    image_matrix = tmp
    Image.fromarray(image_matrix).save("./Results/NoiseOperation_result.bmp")
    
    
    
    

if __name__ == '__main__':
    ImageProcessing()



