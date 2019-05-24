# Untitled - By: oillight - 周三 5月 22 2019

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
#sensor.set_auto_exposure(False, 5000)
#sensor.set_auto_gain(False,30)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    #img = sensor.snapshot()
    img = image.Image("/test.bmp")
    tmp_histogram = img.get_histogram()
    the_threshold = tmp_histogram.get_threshold()
    tmp_statistics = tmp_histogram.get_statistics()
    threshold_l = tmp_statistics.l_mean()
    threshold_a = tmp_statistics.a_mean()
    threshold_b = tmp_statistics.b_mean()
    #threshold_l = the_threshold.l_value()
    #threshold_a = the_threshold.a_value()
    #threshold_b = the_threshold.b_value()
    img.binary([(threshold_l,100,threshold_a,127,threshold_b,-128)])
    img.open(1)
    print("l:"+str(threshold_l)+" a:"+str(threshold_a)+" b:"+str(threshold_b))

    #lines = img.find_lines((0,0,80,60),2,1,100)
    #if lines:
        #for the_line in lines:
            #img.draw_line(the_line.line())
    #img.find_edges(image.EDGE_SIMPLE)
    print(clock.fps())
