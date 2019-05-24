# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, json, pyb, math

#from pyb import UART

sensor.reset()                      # Reset and initialize the sensor.
#sensor.set_auto_exposure(False, 500)
sensor.set_auto_whitebal(True)
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)   # Set frame size to QVGA (320x240) QQVGA(160x120)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

#pyb.LED(1).on()
#pyb.LED(2).on()
#pyb.LED(3).on()

#gray_threshold = [(205,245)]
#lab_threshold = [(78, 100, -35, 126, -7, 27)]

biggist = 0
g_max = 0

distance = 10
g_Range = 5
blobs = []

area_one = (410,500)
area_ten = (690,710)
area_seven = (500,600)


count = 0
theta = None
rho = None
intersection = None

thetas = []
rhos = []

uart = pyb.UART(3, 115200)


while(True):
    clock.tick()                    # Update the FPS clock.
    src_img = sensor.snapshot()#.binary(g_threshold)         # Take a picture and return the image.





    #corr_img = src_img.lens_corr(1.5)
    #mean_img = src_img.mean(1)

    #tmp_img = tmp_img.binary(lab_threshold)
    #tmp_img = tmp_img.open(1)
    #temp_blobs = tmp_img.find_blobs(gray_threshold,False,(0,0,319,239))

    tmp_img = src_img
    tmp_histogram = tmp_img.histogram()
    tmp_threshold = tmp_histogram.get_threshold().value()
    gray_threshold = [(tmp_threshold,255)]
    tmp_img.binary([(tmp_threshold,255)])
    #print(str(tmp_threshold))

    if tmp_threshold>50:
        temp_blobs = tmp_img.find_blobs(gray_threshold,False,(0,0,159,119))

        if temp_blobs:
            for j in range(len(temp_blobs)):
                if temp_blobs[j][4] > biggist:
                    biggist = temp_blobs[j][4]
                    g_max = j

            my_blob = temp_blobs.pop(g_max)

            density = my_blob.density()
            area = my_blob.area()
            rotation = my_blob.rotation()
            text = str(density)+' '+str(area)+' '+str(rotation)

            #print(text)
            tmp_img.draw_rectangle(my_blob.rect(),127)
            my_line = tmp_img.get_regression(gray_threshold,False,my_blob.rect())

            if my_line:
                theta = my_line.theta()
                rho = my_line.rho()
                print("theta: "+str(theta))
                print("rho: "+str(rho))

                #lanes identification
                top_blobs = tmp_img.find_blobs(gray_threshold,False,(distance+g_Range,distance,80-(2*(g_Range+distance)),g_Range),2,1)
                if top_blobs:
                    #print('top')
                    for t in top_blobs:
                        tmp_img.draw_rectangle(t.rect(),127)
                    count += 1
                left_blobs = tmp_img.find_blobs(gray_threshold,False,(distance,distance+g_Range,g_Range,60-(2*(g_Range+distance))),2,1)
                if left_blobs:
                    #print('left')
                    for l in left_blobs:
                        tmp_img.draw_rectangle(l.rect(),127)
                    count += 1
                bottom_blobs = tmp_img.find_blobs(gray_threshold,False,(distance+g_Range,59-distance-g_Range,80-(2*(g_Range+distance)),g_Range),2,1)
                if bottom_blobs:
                    #print('bottom')
                    for b in bottom_blobs:
                        tmp_img.draw_rectangle(b.rect(),127)
                    count += 1
                right_blobs = tmp_img.find_blobs(gray_threshold,False,(79-distance-g_Range,distance+g_Range,g_Range,60-(2*(g_Range+distance))),2,1)
                if right_blobs:
                    #print('right')
                    for r in right_blobs:
                        tmp_img.draw_rectangle(r.rect(),127)
                    count += 1

                if count == 2:
                    if (top_blobs and bottom_blobs) or (right_blobs and left_blobs):
                        intersection = 1
                    elif (top_blobs and right_blobs) or (top_blobs and left_blobs) or (bottom_blobs and right_blobs) or (bottom_blobs and left_blobs):
                        intersection = 2
                elif count == 4:
                    intersection = 3
                else:
                    intersection =0

                #filter
                if (len(thetas) > 11) and (len(rhos) > 11):
                    del thetas[0]
                    del rhos[0]

                    thetas.append(theta)
                    rhos.append(rho)

                    sorted(thetas)
                    sorted(rhos)

                    my_sum = 0
                    tmps = thetas[1:12]
                    for tmp in tmps:
                        my_sum += tmp
                    theta = my_sum / len(thetas)

                    tmps = rhos[1:12]
                    for tmp in tmps:
                        my_sum += tmp
                    rho = my_sum / len(rhos)
                else:
                    thetas.append(theta)
                    rhos.append(rho)
                output_str = "$%d,%d,%d" % (theta,rho,intersection)

            else:
                output_str = "$n"

            tmp_img.draw_line(my_line.line(),127)

        else:
            output_str = "$n"

        tmp_img.draw_rectangle(my_blob.rect(),127)

    else:
        output_str = "$n"

    print(output_str)

    #print(json.dumps(obj))
    uart.write('\n'+output_str)



    #tmp_img.draw_rectangle(distance+g_Range,distance,80-(2*(g_Range+distance)),g_Range)
    #tmp_img.draw_rectangle(distance,distance+g_Range,g_Range,60-(2*(g_Range+distance)))
    #tmp_img.draw_rectangle(distance+g_Range,59-distance-g_Range,80-(2*(g_Range+distance)),g_Range)
    #tmp_img.draw_rectangle(79-distance-g_Range,distance+g_Range,g_Range,60-(2*(g_Range+distance)))



    g_max = 0
    biggist = 0
    count = 0

    #print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    ## to the IDE. The FPS should increase once disconnected.
