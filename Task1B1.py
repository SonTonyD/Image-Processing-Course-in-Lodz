from PIL import Image
import numpy as np
import click

@click.group()
def ImageProcessing():
    pass

@ImageProcessing.command()
@click.option('--name', default="./Images/lenac.bmp", help='path of the image. Example:--name="./Images/lenac.bmp"  ')
@click.option('--brightness', default=0, help='Set the brightness intensity: positive number to increase it and negative to decrease.')
@click.option('--contrast', default=1.0, help='Set the contrast intensity: Can only take positive number. contrast<1 to decrease and contrast >1 to increase')
@click.option('--negative', default=-1.0, help='Set the negative intensity: Can only take positive number. negative<1 to decrease and negative >1 to increase')
def ElementaryOperation(name, brightness, contrast, negative):
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
def GeometricOperation(name, hflip, vflip, dflip, shrink):
    img = Image.open(name)
    image_matrix = np.array(img)
    tmp = np.array(img)
    
    
    
    width = image_matrix.shape[0]
    height = image_matrix.shape[1]
    
    if shrink != 1:
        width = round(image_matrix.shape[0]/shrink)
        height = round(image_matrix.shape[1]/shrink)
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
                    tmp[i,j,k] = image_matrix[(iParamA+iParamB*i)*shrink, (jParamA+jParamB*j)*shrink ,k]          
    else:
        for i in range(width):
            for j in range(height):
                tmp[i,j] = image_matrix[(iParamA+iParamB*i)*shrink, (jParamA+jParamB*j)*shrink ,k]  
    image_matrix = tmp
    Image.fromarray(image_matrix).save("./Results/GeometricOperation_result.bmp")



if __name__ == '__main__':
    ImageProcessing()



