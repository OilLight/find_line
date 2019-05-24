# Untitled - By: oillight - 周六 4月 6 2019

import  image
from resize import reSize

def unevenLightCompensate(input_img,blockSize):
    width = input_img.width()
    height = input_img.height()
    tmp_statistics = input_img.get_statistics([(0, 255)])
    average = tmp_statistics.mean()

    tmp_img = input_img.mean_pooled(blockSize,blockSize)

    for i in range(tmp_img.width()):
        for j in range(tmp_img.height()):
            tmp_pixel = tmp_img.get_pixel(i,j)
            tmp_pixel -= average
            if tmp_pixel < 0:
                tmp_pixel = 0
            if tmp_pixel > 255:
                tmp_pixel = 255
            tmp_img.set_pixel(i,j,tmp_pixel)
	    print(str(i)+' '+str(j))

    tmp_img = reSize(tmp_img,input_img, width, height)
    print(tmp_img.width())
    print(tmp_img.height())

    output_img = input_img.sub(tmp_img)
    #output_img = tmp_img

    return output_img
