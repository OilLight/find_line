# Untitled - By: oillight - 周一 4月 8 2019

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    for i in range(6):
        temp_blobs = src_img.find_blobs(g_threshold,False,(0,i*40,320,40),80,32)
        if temp_blobs:
            for j in range(len(temp_blobs)):
                if temp_blobs[j][4] > biggist:
                    biggist = temp_blobs[j][4]
                    g_max = j
            blobs.append(temp_blobs[g_max])

    if blobs:
        for my_blob in blobs:
            src_img.draw_rectangle(my_blob.rect())
            src_img.draw_cross(my_blob[5],my_blob[6])


    blobs.clear()
    print(clock.fps())
