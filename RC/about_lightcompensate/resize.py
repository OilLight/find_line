# Untitled - By: oillight - 周六 4月 6 2019

import image, sensor,math

def reSize(input_img, tmp_img,width, height):
    fx = input_img.width()/width
    fy = input_img.height()/height

    dst_img = tmp_img.copy()

    for i in range(height):
        srcy = i / fy
        y = math.floor(srcy)
        v = srcy - y
        if v < 0:
            y = 0
            v = 0

        if y >= input_img.height() - 1:
            y = input_img.height() - 2
            v = 1

        for j in range(width):
            srcx = j / fx
            x = math.floor(srcx)
            u = srcx - x
            if x < 0:
                x = 0
                u = 0

            if x >= input_img.width() - 1:
                x = input_img.width() - 2
                u = 1

            pixel = (1 - u) * (1 - v) * input_img.get_pixel(x, y) + (1 - u) * v *  input_img.get_pixel(x, y+1) + u *(1 - v) * input_img.get_pixel(x+1, y) + u * v * input_img.get_pixel(x+1, y+1)
            if pixel<0:
                pixel = 0
            if pixel>255:
                pixel =255

            pixel = round(pixel)
 
            dst_img.set_pixel(j,i,pixel)

    return dst_img
