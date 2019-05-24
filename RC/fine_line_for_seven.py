# Untitled - By: oillight - 周三 4月 10 2019

import sensor, image, time

sensor.reset()
#sensor.set_auto_exposure(False, 800)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

tb = 0
lr = 0

while(True):
    clock.tick()
    src_img = sensor.snapshot()
    corr_img = src_img.lens_corr(1.6)
    tmp_histogram = corr_img.histogram()
    tmp_threshold = tmp_histogram.get_threshold().value()
    gray_threshold = [(tmp_threshold,255)]
    lines = corr_img.find_lines();
    for the_line in lines:
        #corr_img.draw_line(the_line.line())
        print("("+str(the_line.x1())+","+str(the_line.y1())+") ("+str(the_line.x2())+","+str(the_line.y2())+")")

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

    for i in range(len(lines)):
        for j in range(len(lines)):
            if (j+i+1) >= len(lines):
                break

            line1 = lines[i]
            line2 = lines[j+i+1]

            if (line1.x1()==line1.x2()) and (line1.y1()==line1.y2()):
                break
            if (line2.x1()==line2.x2()) and (line2.y1()==line2.y2()):
                break
            theta1 = line1.theta()
            theta2 = line2.theta()
            sub = abs(theta1 - theta2)
            #print(str(sub))
            if 70<sub<105:
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

                mask = True
                if B1 == 0:
                    crossover_x = -C1/A1
                    crossover_y = -(A2*crossover_x+C2)/B2
                    mask = False
                else:
                    k1 = -A1/B1
                    b1 = -C1/B1

                if B2 == 0:
                    crossover_x = -C2/A2
                    crossover_y = -(A1*crossover_x+C1)/B1
                    mask = False
                else:
                    k2 = -A2/B2
                    b2 = -C2/B2

                if mask:
                    crossover_x = int(round((b2 -b1)/(k1 -k2)))
                    crossover_y = int(round(k1*crossover_x+b1))

                print("crossover_point: ("+str(crossover_x)+","+str(crossover_y)+")")
                corr_img.draw_cross(crossover_x,crossover_y)
                #top_point = []
                #bottom_point = []
                #left_point = []
                #right_point = []

                #if (0<=theta1<45) or (135<=theta1<=180):
                    #if line1.y1() < line1.y2():
                        #top_point = point1
                        #bottom_point = point2
                    #else:
                        #bottom_point = point1
                        #top_point = point2
                    #if line2.x1() < line2.x2():
                        #left_point = point3
                        #right_point = point4
                    #else:
                        #right_point = point3
                        #left_point = point4
                #else:
                    #if line2.y1() < line2.y2():
                        #top_point = point3
                        #bottom_point = point4
                    #else:
                        #bottom_point = point3
                        #top_point = point4
                    #if line1.x1() < line1.x2():
                        #left_point = point1
                        #right_point = point2
                    #else:
                        #right_point = point1
                        #left_point = point2

                #print("top_point:"+str(top_point))
                #print("bottom_point:"+str(bottom_point))
                #print("left_point:"+str(left_point))
                #print("right_point:"+str(right_point))

                #if lr:
                    #mid_x2 = (crossover_x + left_point[0])/2
                    #mid_y2 = (crossover_y + left_point[1])/2
                #else:
                    #mid_x2 = (crossover_x + right_point[0])/2
                    #mid_y2 = (crossover_y + right_point[1])/2
                #if tb:
                    #mid_x1 = (crossover_x + top_point[0])/2
                    #mid_y1 = (crossover_y + top_point[1])/2
                #else:
                    #mid_x1 = (crossover_x + bottom_point[0])/2
                    #mid_y1 = (crossover_y + bottom_point[1])/2

                blob1 = []
                blob2 = []
                blob3 = []
                blob4 = []
                blob5 = []
                blob6 = []
                blob7 = []
                blob8 = []
                blobs = [blob1,blob2,blob3,blob4,blob5,blob6,blob7,blob8]
                tmp_img = corr_img.copy()

                for k in range(4):
                    tmp_x = int(round((points[k][0] - crossover_x) *4/5) + crossover_x)
                    tmp_y = int(round((points[k][1] - crossover_y) *4/5) + crossover_y)
                    corr_img.draw_cross(tmp_x,tmp_y)

                    #t = int(tmp_y / 4)
                    #b = int((59 - tmp_y) /4)
                    #l = int(tmp_x /4)
                    #r = int((79 - tmp_x) /4)
                    #print("t: "+str(t)+" b: "+str(b)+" l: "+str(l)+" r: "+str(r))
                    #corr_img.draw_rectangle((tmp_x-l,tmp_y-t,l+r,t+b),127)
                    #blobs[k] = tmp_img.find_blobs(gray_threshold,False,(tmp_x-l,tmp_y-t,l+r,t+b))
                    input_x = tmp_x-4
                    input_y = tmp_y-4
                    input_w = 8
                    input_h = 8
                    if input_x <0:
                        input_x = 0
                    if input_y <0:
                        input_y = 0
                    if tmp_x+4 >79:
                        input_w = 8-(tmp_x+4-79)
                    if tmp_y+4 >59:
                        input_h = 8-(tmp_y+4-59)
                    blobs[k] = tmp_img.find_blobs(gray_threshold,False,(input_x,input_y,input_w,input_h))
                    corr_img.draw_rectangle((input_x,input_y,input_w,input_h),127)

                    tmp_x = int(round((points[k][0] - crossover_x) /3) + crossover_x)
                    tmp_y = int(round((points[k][1] - crossover_y) /3) + crossover_y)
                    corr_img.draw_cross(tmp_x,tmp_y)
                    input_x = tmp_x-4
                    input_y = tmp_y-4
                    input_w = 8
                    input_h = 8
                    if input_x <0:
                        input_x = 0
                    if input_y <0:
                        input_y = 0
                    if tmp_x+4 >79:
                        input_w = 8-(tmp_x+4-79)
                    if tmp_y+4 >59:
                        input_h = 8-(tmp_y+4-59)
                    print("tmp_x:"+str(tmp_x)+" tmp_y:"+str(tmp_y))
                    print("x:"+str(input_x)+" y:"+str(input_y)+" w:"+str(input_w)+" h:"+str(input_h))
                    print("k:"+str(k))
                    blobs[k+4] = tmp_img.find_blobs(gray_threshold,False,(input_x,input_y,input_w,input_h))
                    corr_img.draw_rectangle((input_x,input_y,input_w,input_h),127)


                    #for the_blob in blobs[k]:
                        #corr_img.draw_rectangle(the_blob.rect())
                if blobs[0] and blobs[4]:
                    if ((blobs[0][0].y()+8)<blobs[4][0].y()) or (blobs[0][0].y()>(blobs[4][0].y()+8)) or ((blobs[0][0].x()+8)<blobs[4][0].x()) or (blobs[0][0].x()>(blobs[4][0].x()+8)):
                        mid_x1 = (crossover_x + point1[0])/2
                        mid_y1 = (crossover_y + point1[1])/2
                    else:
                        continue
                elif blobs[1] and blobs[5]:
                    if ((blobs[1][0].y()+8)<blobs[5][0].y()) or (blobs[1][0].y()>(blobs[5][0].y()+8)) or ((blobs[1][0].x()+8)<blobs[5][0].x()) or (blobs[1][0].x()>(blobs[5][0].x()+8)):
                        mid_x1 = (crossover_x + point2[0])/2
                        mid_y1 = (crossover_y + point2[1])/2
                    else:
                        continue
                else:
                    continue
                if blobs[2] and blobs[6]:
                    if ((blobs[2][0].y()+7)<blobs[6][0].y()) or (blobs[2][0].y()>(blobs[6][0].y()+8)) or ((blobs[2][0].x()+8)<blobs[6][0].x()) or (blobs[2][0].x()>(blobs[6][0].x()+8)):
                        mid_x2 = (crossover_x + point3[0])/2
                        mid_y2 = (crossover_y + point3[1])/2
                    else:
                        continue

                elif blobs[3] and blobs[7]:
                    if ((blobs[3][0].y()+7)<blobs[7][0].y()) or (blobs[3][0].y()>(blobs[7][0].y()+8)) or ((blobs[3][0].x()+8)<blobs[7][0].x()) or (blobs[3][0].x()>(blobs[7][0].x()+8)):
                        mid_x2 = (crossover_x + point4[0])/2
                        mid_y2 = (crossover_y + point4[1])/2
                    else:
                        continue
                else:
                    continue
                dst_x1 = round(mid_x1)
                dst_y1 = round(mid_y1)
                dst_x2 = round(mid_x2)
                dst_y2 = round(mid_y2)

                corr_img.draw_line((dst_x1,dst_y1,dst_x2,dst_y2),127)


            else:
                print("none")

    print("length: "+str(len(lines)))

    print(clock.fps())
    print(" ")
