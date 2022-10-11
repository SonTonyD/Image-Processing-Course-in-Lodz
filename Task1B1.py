from PIL import Image
import numpy as np
import click

@click.command()
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
    Image.fromarray(image_matrix).save("./Results/B1_result.bmp")


if __name__ == '__main__':
    ElementaryOperation()



