# Untitled - By: oillight - 周三 4月 10 2019
# There are a big error in the program, the filter would give the wrong rho.
import sensor, image, time, math
from pyb import UART
sensor.reset()
#sensor.set_auto_exposure(False, 800)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
uart = UART(3, 115200)
count1 = 0
count2 = 0
theta = None
rho = None
intersection = None
thetas = []
rhos = []
last = []
last_str ="$n"
mask_straight = True
mask_none = True
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
        print("length: "+str(len(lines)))
        for i in range(len(lines)):
            for j in range(len(lines)):
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
                    corr_img.draw_line(line1.line(),127)
                    corr_img.draw_line(line2.line(),127)
                    crossover_x = 0
                    crossover_y = 0
                    point1 = [line1.x1(),line1.y1()]
                    point2 = [line1.x2(),line1.y2()]
                    point3 = [line2.x1(),line2.y1()]
                    point4 = [line2.x2(),line2.y2()]
                    points = [point1,point2,point3,point4]
                    A1 = point1[1] - point2[1]
                    B1 = point2[0] - point1[0]
                    C1 = point1[0]*point2[1] - point1[1]*point2[0]

                    A2 = point3[1] - point4[1]
                    B2 = point4[0] - point3[0]
                    C2 = point3[0]*point4[1] - point3[1]*point4[0]
                    #print(str(A1)+" "+str(B1)+" "+str(C1))
                    #print(str(A2)+" "+str(B2)+" "+str(C2))
                    mask = True
                    if B1 == 0:
                        crossover_x = -C1/A1
                        crossover_y = -(A2*crossover_x+C2)/B2
                        mask = False
                    else:
                        k1 = -A1/B1
                        b1 = -C1/B1
                        #print(str(k1)+" "+str(b1))
                    if B2 == 0:
                        crossover_x = -C2/A2
                        crossover_y = -(A1*crossover_x+C1)/B1
                        mask = False
                    else:
                        k2 = -A2/B2
                        b2 = -C2/B2
                        #print(str(k2)+" "+str(b2))
                    if mask:
                        crossover_x = (b2 -b1)/(k1 -k2)
                        crossover_y = k1*crossover_x+b1
                    # exclude out of range crossover point
                    if crossover_x<0 or crossover_x>79 or crossover_y<0 or crossover_y>59:
                        continue
                    #print("crossover_point: ("+str(crossover_x)+","+str(crossover_y)+")")
                    corr_img.draw_cross(int(crossover_x),int(crossover_y))
                    ##discriminate intersection
                    blobs = [[],[],[],[],[],[],[],[]]
                    tmp_img = corr_img.copy()
                    for k in range(4):
                        #closer range
                        tmp_x = int(round((points[k][0] - crossover_x) *4/5) + crossover_x)
                        tmp_y = int(round((points[k][1] - crossover_y) *4/5) + crossover_y)
                        corr_img.draw_cross(tmp_x,tmp_y)
                        input_x = tmp_x-5
                        input_y = tmp_y-5
                        input_w = 10
                        input_h = 10
                        if input_x <0:
                            input_x = 0
                        if input_y <0:
                            input_y = 0
                        if tmp_x+5 >79:
                            input_w = 10-(tmp_x+5-79)
                        if tmp_y+5 >59:
                            input_h = 10-(tmp_y+5-59)
                        blobs[k] = tmp_img.find_blobs(gray_threshold,False,(input_x,input_y,input_w,input_h))
                        corr_img.draw_rectangle((input_x,input_y,input_w,input_h),127)
                        #further range
                        tmp_x = int(round((points[k][0] - crossover_x) /3) + crossover_x)
                        tmp_y = int(round((points[k][1] - crossover_y) /3) + crossover_y)
                        corr_img.draw_cross(tmp_x,tmp_y)
                        input_x = tmp_x-5
                        input_y = tmp_y-5
                        input_w = 10
                        input_h = 10
                        if input_x <0:
                            input_x = 0
                        if input_y <0:
                            input_y = 0
                        if tmp_x+5 >79:
                            input_w = 10-(tmp_x+5-79)
                        if tmp_y+5 >59:
                            input_h = 10-(tmp_y+5-59)
                        #print("tmp_x:"+str(tmp_x)+" tmp_y:"+str(tmp_y))
                        #print("x:"+str(input_x)+" y:"+str(input_y)+" w:"+str(input_w)+" h:"+str(input_h))
                        #print("k:"+str(k))
                        blobs[k+4] = tmp_img.find_blobs(gray_threshold,False,(input_x,input_y,input_w,input_h))
                        corr_img.draw_rectangle((input_x,input_y,input_w,input_h),127)
                        #for the_blob in blobs[k]:
                            #corr_img.draw_rectangle(the_blob.rect())
                    # discriminate first line
                    if blobs[0] and blobs[4]:
                        if ((blobs[0][0].y()+8)<blobs[4][0].y()) or (blobs[0][0].y()>(blobs[4][0].y()+8)) or ((blobs[0][0].x()+8)<blobs[4][0].x()) or (blobs[0][0].x()>(blobs[4][0].x()+8)):
                            mid_x1 = (crossover_x + point1[0])/2
                            mid_y1 = (crossover_y + point1[1])/2
                            count1 +=1
                    if blobs[1] and blobs[5]:
                        if ((blobs[1][0].y()+8)<blobs[5][0].y()) or (blobs[1][0].y()>(blobs[5][0].y()+8)) or ((blobs[1][0].x()+8)<blobs[5][0].x()) or (blobs[1][0].x()>(blobs[5][0].x()+8)):
                            mid_x1 = (crossover_x + point2[0])/2
                            mid_y1 = (crossover_y + point2[1])/2
                            count1 +=1
                    # discriminate seacon line
                    if blobs[2] and blobs[6]:
                        if ((blobs[2][0].y()+7)<blobs[6][0].y()) or (blobs[2][0].y()>(blobs[6][0].y()+8)) or ((blobs[2][0].x()+8)<blobs[6][0].x()) or (blobs[2][0].x()>(blobs[6][0].x()+8)):
                            mid_x2 = (crossover_x + point3[0])/2
                            mid_y2 = (crossover_y + point3[1])/2
                            count2 +=1
                    if blobs[3] and blobs[7]:
                        if ((blobs[3][0].y()+7)<blobs[7][0].y()) or (blobs[3][0].y()>(blobs[7][0].y()+8)) or ((blobs[3][0].x()+8)<blobs[7][0].x()) or (blobs[3][0].x()>(blobs[7][0].x()+8)):
                            mid_x2 = (crossover_x + point4[0])/2
                            mid_y2 = (crossover_y + point4[1])/2
                            count2 +=1
                    #discriminate intersection
                    print(str(count1+count2))
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
                            corr_img.draw_line((dst_x1,dst_y1,dst_x2,dst_y2),127)

                            point1 = [dst_x1,dst_y1]
                            point2 = [dst_x2,dst_y2]

                            A3 = point1[1] - point2[1]
                            B3 = point2[0] - point1[0]
                            C3 = point1[0]*point2[1] - point1[1]*point2[0]

                            if B3 == 0:
                                rho = point1[0]
                                theta = 0
                            else:
                                k3 = -A3/B3
                                b3 = -C3/B3
                                if k3!= 0:
                                    k4 = -(1/k3)
                                    b4 = 0
                                    crossover_x = (b4 -b3)/(k3 -k4)
                                    crossover_y = k3*crossover_x+b3
                                else:
                                    crossover_x = 0
                                    crossover_y = b3
                                #print("crossover_x:"+str(crossover_x)+" crossover_y:"+str(crossover_y))
                                rho = math.sqrt(crossover_x**2 + crossover_y**2)
                                theta = math.atan2(crossover_y, crossover_x)*180/math.pi
                                if theta<0:
                                    theta+=180
                                #filter
                                if (len(thetas) > 39) and (len(rhos) > 39):
                                    del thetas[0]
                                    del rhos[0]

                                    thetas.append(theta)
                                    rhos.append(rho)

                                    sorted(thetas)
                                    sorted(rhos)

                                    my_sum = 0
                                    tmps = thetas[1:40]
                                    for tmp in tmps:
                                        my_sum += tmp
                                    theta = my_sum / len(thetas)

                                    tmps = rhos[1:40]
                                    for tmp in tmps:
                                        my_sum += tmp
                                    rho = my_sum / len(rhos)
                                else:
                                    thetas.append(theta)
                                    rhos.append(rho)
                                last = [theta,rho]
                                output_str = "$%d,%d,%d" % (theta,rho,intersection)
                                mask_none = True
                    elif (count1+count2)==4:
                        intersection = 3
                        output_str = "$N,N,%d" % (intersection)
                        mask_none = True
                        thetas.clear()
                        rhos.clear()
                    else:
                        print("t1")
                        mask_none = False
                        output_str = last_str
                else:
                    print("t2")
                    mask_none = False
                    output_str = last_str
        if mask_straight:
            print("d")
            if len(lines) > 1:
                sum_theta = 0
                sum_rho = 0
                for the_line in lines:
                    sum_theta += the_line.theta()
                    sum_rho += the_line.rho()
                    corr_img.draw_line(the_line.line())
                theta = sum_theta/len(lines)
                rho = sum_rho/len(lines)
            else:
                theta = lines[0].theta()
                rho = lines[0].rho()
            if (len(thetas) > 39) and (len(rhos) > 39):
                del thetas[0]
                del rhos[0]

                thetas.append(theta)
                rhos.append(rho)

                sorted(thetas)
                sorted(rhos)

                my_sum = 0
                tmps = thetas[1:40]
                for tmp in tmps:
                    my_sum += tmp
                theta = my_sum / len(thetas)

                tmps = rhos[1:40]
                for tmp in tmps:
                    my_sum += tmp
                rho = my_sum / len(rhos)
            else:
                thetas.append(theta)
                rhos.append(rho)
            intersection = 1
            last = [theta,rho]
            output_str = "$%d,%d,%d" % (theta,rho,intersection)
            mask_none = True
    else:
        print("t3")
        mask_none = False
        output_str = last_str

    print (output_str)
    if mask_none:
        last_str = output_str
    count1 = 0
    count2 = 0
    mask_straight = True
    uart.write(output_str)
    print(clock.fps())
    print(" ")
