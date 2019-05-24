# Untitled - By: oillight - 周日 4月 21 2019


import sensor, image, time, math
from pyb import UART
sensor.reset()
#sensor.set_auto_exposure(False, 800)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()




def get_average(data):
    average = sum(data) / len(data)
    average = round(average)
    return average



def filter(data):
    length = len(data)
    if length >2:
        sorted(data)
        tmps = data[1:length]
    else:
        tmps = data
    average = get_average(tmps)

    return average



def control_oscillations(data,datum,length):
    if (len(data) >= length):
        del data[0]
    data.append(datum)
    output_value = filter(data)
    return output_value


def find_biggest_blob(blobs):
    biggest = 0
    the_max = 0
    for i in range(len(blobs)):
        if temp_blobs[i][4] > biggist:
            biggist = temp_blobs[i][4]
            the_max = i

    biggest_blob = temp_blobs[the_max]
    return biggest_blob

def find_equation(points):
    point1 = points[0]
    point2 = points[1]
    output_list = []
    #print("point1:"+str(point1))
    #print("point2:"+str(point2))
    tmp_x = point1[0] - point2[0]
    tmp_y = point1[1] - point2[1]
    if tmp_x != 0:
        k = tmp_y/tmp_x
        b = point1[1] - k*point1[0]
        output_list = [k,b]
    else:
        x = points[0][0]
        output_list = [x]
    return output_list

def get_crosser_point(points1 ,mask=True, points2=[]):
    crossover_x = 0
    crossover_y = 0
    para1 = find_equation(points1)
    #print("para1:"+str(para1))
    if points2:
        para2 = find_equation(points2)
        if len(para1) == 2 and len(para2) == 2:
            crossover_x = (para2[1]-para1[1])/(para1[0]-para2[0])
            crossover_y =  para1[0]*crossover_x+para1[1]
        else:
            if len(para1) == 1:
                crossover_x = para1[0]
                crossover_y = para2[1]
            else:
                crossover_x = para2[0]
                crossover_y = para1[1]
    else:
        if len(para1) == 2:
            if para1[0] != 0:
                k = -1/para1[0]
                if mask:
                    b = 0
                else:
                    b = 0-79*k
                para2 = [k,b]
                crossover_x = (para1[1]-b)/(k-para1[0])
                crossover_y =  k*crossover_x+b
            else:
                if mask:
                    crossover_x = 0
                else:
                    crossover_x = 79
                crossover_y = para1[1]
        else:
            crossover_x = para1[0]
            crossover_y = 0
    #print("m crossover_point: ("+str(crossover_x)+","+str(crossover_y)+")")
    crossover_point = [crossover_x,crossover_y]
    return crossover_point


def find_distance(point1, point2):
    distance = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    return distance

def get_rho(point):
    origin_point = [0,0]
    rho = find_distance(point,origin_point)
    return rho

def get_theta(point):
    theta = math.atan2(point[1], point[0])*180/math.pi
    if theta<0:
        theta += 180
    return theta

def get_para_of_line(points):
    tmp_y = points[0][1] - points[1][1]
    tmp_x = points[0][0] - points[1][0]
    if tmp_x !=0:
        k = tmp_y/tmp_x
        crossover_point = get_crosser_point(points)
        if k > 0:
            crossover_point_anti = get_crosser_point(points,False)
            rho = get_rho(crossover_point_anti)
        else:
            rho = get_rho(crossover_point)
        theta = get_theta(crossover_point)
    else:
        rho = points[0][0]
        theta = 0
    para = [theta,rho]
    return para

def range_check(img,threshoid,crosser_point, end_point, ratio, the_range=10):
    tmp_x = int(round((end_point[0] - crosser_point[0]) *ratio + crosser_point[0]))
    tmp_y = int(round((end_point[1] - crosser_point[1]) *ratio + crosser_point[1]))
    img.draw_cross(tmp_x,tmp_y)
    half_range = int(the_range/2)
    input_x = tmp_x-half_range
    input_y = tmp_y-half_range
    input_w = the_range
    input_h = the_range
    if input_x <0:
        input_x = 0
    if input_y <0:
        input_y = 0
    if tmp_x+half_range >79:
        input_w = 10-(tmp_x+half_range-79)
    if tmp_y+half_range >59:
        input_h = 10-(tmp_y+half_range-59)
    blobs = img.find_blobs(threshoid,False,(input_x,input_y,input_w,input_h))
    img.draw_rectangle((input_x,input_y,input_w,input_h),127)
    return blobs

def overlap_check(blob1,blob2):
    if((blob1[0].y()+8)<blob2[0].y()) or (blob1[0].y()>(blob2[0].y()+8)) or ((blob1[0].x()+8)<blob2[0].x()) or (blob1[0].x()>(blob2[0].x()+8)):
        return True
    else:
        return False


uart = UART(3, 115200)
count1 = 0
count2 = 0
count3 = 0
theta = None
rho = None
intersection = None
thetas = []
rhos = []
thresholds = []
last = []
last_list =[999,999,0]
mask_straight = True
mask_none = False
output_str =" "
while(True):
    clock.tick()
    src_img = sensor.snapshot()
    corr_img =src_img.lens_corr(1.6)
    #corr_img.mean(1)
    tmp_histogram = corr_img.histogram()
    tmp_threshold = tmp_histogram.get_threshold().value()
    tmp_threshold = control_oscillations(thresholds,tmp_threshold,40)
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
            if mask_none:
                break
            for j in range(len(lines)):
                if mask_none:
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
                    corr_img.draw_cross(int(crossover_x),int(crossover_y),127)
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
                            corr_img.draw_line((dst_x1,dst_y1,dst_x2,dst_y2),127)

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
            true_lines = []
            for the_line in lines:
                crossover_point = [(the_line.x1() + the_line.x2())/2,(the_line.y1() + the_line.y2())/2]
                point_t = [the_line.x1(),the_line.y1()]
                point_b = [the_line.x2(),the_line.y2()]
                blobs = []
                blobs_t_c = range_check(corr_img,gray_threshold,crossover_point,point_t,0.33)
                blobs_t_f = range_check(corr_img,gray_threshold,crossover_point,point_t,0.8)
                blobs_b_c = range_check(corr_img,gray_threshold,crossover_point,point_b,0.33)
                blobs_b_f = range_check(corr_img,gray_threshold,crossover_point,point_b,0.8)
                #if blobs_t_c and blobs_t_f and blobs_b_c and blobs_b_f:
                    #true_lines.append(the_line)
                if blobs_t_c:
                    count3 += 1
                if blobs_t_f:
                    count3 += 1
                if blobs_b_c:
                    count3 += 1
                if blobs_b_f:
                    count3 += 1
                print(str(count3))
                if count3 >= 3:
                    true_lines.append(the_line)
            if true_lines:
                if len(true_lines) > 1:
                    sum_theta = 0
                    sum_rho = 0
                    for the_line in true_lines:
                        sum_theta += the_line.theta()
                        if the_line.theta()<=90:
                            sum_rho += the_line.rho()
                        else:
                            points = [[the_line.x1(),the_line.y1()],[the_line.x2(),the_line.y2()]]
                            crossover_point = get_crosser_point(points,False)
                            sum_rho += get_rho(crossover_point)
                        corr_img.draw_line(the_line.line())
                    theta = sum_theta/len(lines)
                    rho = sum_rho/len(lines)
                else:
                    corr_img.draw_line(true_lines[0].line())
                    theta = true_lines[0].theta()
                    if theta<=90:
                        rho = true_lines[0].rho()
                    else:
                        points = [[true_lines[0].x1(),true_lines[0].y1()],[true_lines[0].x2(),true_lines[0].y2()]]
                        crossover_point = get_crosser_point(points,False)
                        rho = get_rho(crossover_point)
                theta = control_oscillations(thetas,theta,80)
                rho = control_oscillations(rhos,rho,80)
                intersection = 1
                last = [theta,rho]
                output_list = [theta,rho,intersection]
                mask_none = True
            else:
                print("no right lines")
                mask_none = False
                output_list = last_list

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
    print(output_str)
    count1 = 0
    count2 = 0
    count3 = 0
    mask_straight = True
    mask_none = False
    uart.write(output_str)
    print(clock.fps())
    print(" ")

