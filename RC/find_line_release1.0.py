# Untitled - By: oillight - 周六 4月 20 2019
import sensor, image, time, math
from pyb import UART
from about2 import get_average
from about2 import filter
from about2 import control_oscillations
from about2 import find_equation
from about2 import get_crosser_point
from about2 import find_distance
from about2 import get_rho
from about2 import get_theta
from about2 import get_para_of_line
from about2 import range_check
from about2 import overlap_check
sensor.reset()
#sensor.set_auto_exposure(False, 800)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

uart = UART(3, 115200)
clock = time.clock()
count1 = 0
count2 = 0
theta = None
rho = None
intersection = None
thetas = []
rhos = []
last = []
last_list =[999,999,0]
mask_straight = True
mask_none = False
output_str =" "
while(True):
    clock.tick()
    src_img = sensor.snapshot()
    corr_img =src_img.lens_corr(1.6)
    corr_img.mean(1)
    tmp_histogram = corr_img.histogram()
    tmp_threshold = tmp_histogram.get_threshold().value()
    gray_threshold = [(tmp_threshold,255)]
    lines = src_img.find_lines();
    #for the_line in lines:
        #corr_img.draw_line(the_line.line())
        #print("("+str(the_line.x1())+","+str(the_line.y1())+") ("+str(the_line.x2())+","+str(the_line.y2())+")")
    if lines:
        for ii in range(len(lines)):
            for jj in range(len(lines)):
                if (jj+ii+1) >= len(lines):
                    break
                line1 = lines[ii]
                line2 = lines[jj+ii+1]

                if abs(line1.theta()-line2.theta())<=10:
                    #print(str(abs(line1.theta()-line2.theta())))
                    if abs (line1.rho()-line2.rho())<=10:
                        #print(str(abs(line1.theta()-line2.theta())))
                        del lines[jj+ii+1]
        #print("length: "+str(len(lines)))
        for i in range(len(lines)):
            if mask_none :
                break
            for j in range(len(lines)):
                if mask_none :
                    break
                if (j+i+1) >= len(lines):
                    break
                line1 = lines[i]
                line2 = lines[j+i+1]
                #exclude point
                if (line1.x1()==line1.x2()) and (line1.y1()==line1.y2()):
                    continue
                if (line2.x1()==line2.x2()) and (line2.y1()==line2.y2()):
                    continue
                #fine perpendicular lines or 45 degree angle
                theta1 = line1.theta()
                theta2 = line2.theta()
                sub = abs(theta1 - theta2)
                #print(str(sub))
                if 70<sub<105 or 40<sub<50:
                    mask_straight = False
                    ##fine crossover point
                    #corr_img.draw_line(line1.line(),127)
                    #corr_img.draw_line(line2.line(),127)
                    points1 = [[line1.x1(),line1.y1()],[line1.x2(),line1.y2()]]
                    points2 = [[line2.x1(),line2.y1()],[line2.x2(),line2.y2()]]
                    points = [points1[0],points1[1],points2[0],points2[1]]
                    crossover_point = []
                    crossover_point = get_crosser_point(points1,True,points2)
                    crossover_x = crossover_point[0]
                    crossover_y = crossover_point[1]
                    #corr_img.draw_cross(int(crossover_x),int(crossover_y),127)
                    # exclude out of range crossover point
                    if crossover_x<0 or crossover_x>79 or crossover_y<0 or crossover_y>59:
                        continue
                    #corr_img.draw_cross(int(crossover_x),int(crossover_y))
                    ##discriminate intersection
                    blobs = [[],[],[],[],[],[],[],[]]
                    for k in range(4):
                        #closer range
                        blobs[k] = range_check(corr_img,gray_threshold,crossover_point,points[k],0.33)
                        #further range
                        blobs[k+4] = range_check(corr_img,gray_threshold,crossover_point,points[k],0.8)
                    # discriminate first line
                    if blobs[0] and blobs[4]:
                        if overlap_check(blobs[0],blobs[4]):
                            mid_x1 = (crossover_x + points1[0][0])/2
                            mid_y1 = (crossover_y + points1[0][1])/2
                            count1 +=1
                    if blobs[1] and blobs[5]:
                        if overlap_check(blobs[1],blobs[5]):
                            mid_x1 = (crossover_x + points1[1][0])/2
                            mid_y1 = (crossover_y + points1[1][1])/2
                            count1 +=1
                    # discriminate seacon line
                    if blobs[2] and blobs[6]:
                        if overlap_check(blobs[2],blobs[6]):
                            mid_x2 = (crossover_x + points2[0][0])/2
                            mid_y2 = (crossover_y + points2[0][1])/2
                            count2 +=1
                    if blobs[3] and blobs[7]:
                        if overlap_check(blobs[3],blobs[7]):
                            mid_x2 = (crossover_x + points2[1][0])/2
                            mid_y2 = (crossover_y + points2[1][1])/2
                            count2 +=1
                    #discriminate intersection
                    if (count1+count2)==2:
                        #"7"">"
                        if count1==1 and count2==1:
                            if 70<sub<105:
                                intersection = 2
                            if 40<sub<50:
                                intersection = 4
                            dst_x1 = round(mid_x1)
                            dst_y1 = round(mid_y1)
                            dst_x2 = round(mid_x2)
                            dst_y2 = round(mid_y2)
                            #corr_img.draw_line((dst_x1,dst_y1,dst_x2,dst_y2),127)

                            points = [[dst_x1,dst_y1],[dst_x2,dst_y2]]
                            para = get_para_of_line(points)
                            theta = para[0]
                            rho = para[1]
                            #filter
                            theta = control_oscillations(thetas,theta,40)
                            rho = control_oscillations(rhos,rho,40)
                            last = [theta,rho]
                            output_list = [theta,rho,intersection]
                            mask_none = True
                    elif (count1+count2)==4:
                        intersection = 3
                        output_list = [999,999,intersection]
                        mask_none = True
                        thetas.clear()
                        rhos.clear()
                    else:
                        #print("number of lines is wrong")
                        mask_none = False
                        output_list = last_list
                else:
                    #print("no right angle lines")
                    mask_none = False
                    output_list = last_list
        if mask_straight:
            #print("d")
            if len(lines) > 1:
                sum_theta = 0
                sum_rho = 0
                for the_line in lines:
                    sum_theta += the_line.theta()
                    if the_line.theta()<=90:
                        sum_rho += the_line.rho()
                    else:
                        points = [[the_line.x1(),the_line.y1()],[the_line.x2(),the_line.y2()]]
                        crossover_point = get_crosser_point(points,False)
                        sum_rho += get_rho(crossover_point)
                    #corr_img.draw_line(the_line.line())
                theta = sum_theta/len(lines)
                rho = sum_rho/len(lines)
            else:
                #corr_img.draw_line(lines[0].line())
                theta = lines[0].theta()
                if theta<=90:
                    rho = lines[0].rho()
                else:
                    points = [[lines[0].x1(),lines[0].y1()],[lines[0].x2(),lines[0].y2()]]
                    crossover_point = get_crosser_point(points,False)
                    rho = get_rho(crossover_point)

            theta = control_oscillations(thetas,theta,40)
            rho = control_oscillations(rhos,rho,40)

            intersection = 1
            last = [theta,rho]
            output_list = [theta,rho,intersection]
            mask_none = True
    else:
        #print("no lines")
        mask_none = False
        output_list = last_list

    #print (output_list)
    if mask_none:
        last_list = output_list
    if output_list[0]//100 == 0:
        if output_list[0]//10 == 0:
            str_theta = "00%d" % (output_list[0])
        else:
            str_theta = "0%d" % (output_list[0])
    else:
        str_theta = "%d" % (output_list[0])
    if output_list[1]//100 == 0:
        if output_list[1]//10 == 0:
            str_rho = "00%d" % (output_list[1])
        else:
            str_rho = "0%d" % (output_list[1])
    else:
        str_rho = "%d" % (output_list[1])
    str_intersection = str(output_list[2])
    output_str = "$"+str_theta+","+str_rho+","+str_intersection
    #print(output_str)
    count1 = 0
    count2 = 0
    mask_straight = True
    mask_none = False
    uart.write(output_str)
    print(clock.fps())
    print(" ")
