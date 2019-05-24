# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
judge=0
output=[]

while(True):
    clock.tick()                    # Update the FPS clock.
    src_img = sensor.snapshot()         # Take a picture and return the image.

    #src_img.to_grayscale()
    #src_img.binary([(93,100),(-2,5),(-8,1)])
    src_img.binary([(214,249)])
    #src_img.open(1)

    for i in range(0,8):
        pieces_img=src_img.copy((40*i,80,40,80))
        for x in range(0,40):
            for y in range(0,80):
                if pieces_img.get_pixel(x,y)==255:
                    judge=judge+1

        if judge >= 1000:
            output.append(1)
        else:
            output.append(0)
        judge=0


    print(output)
    output.clear()
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
