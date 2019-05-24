# Untitled - By: oillight - 周六 4月 27 2019

import sensor, image, time, math
from pyb import UART,LED
sensor.reset()
sensor.set_auto_exposure(False, 1700)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.set_auto_gain(False,27)
sensor.skip_frames(time = 2000)
led_B = LED(3)
led_G = LED(2)
led_R = LED(1)
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

def weighted_mean(data):
    length = data.len()
    radio = (1+length)*length*0.5
    tmp = 1/radio
    the_sum = 0
    for i in range(10):
        the_sum += data[i]*(i+1)*tmp
    return the_sum


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

def range_check(img,input_threshold,crosser_point, end_point, ratio, the_range=10):
    tmp_x = int(round((end_point[0] - crosser_point[0]) *ratio + crosser_point[0]))
    tmp_y = int(round((end_point[1] - crosser_point[1]) *ratio + crosser_point[1]))
    #img.draw_cross(tmp_x,tmp_y)
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
    blobs = img.find_blobs(input_threshold,False,(input_x,input_y,input_w,input_h))#,2,1,10,20,True)
    img.draw_rectangle((input_x,input_y,input_w,input_h),50)
    return blobs

def overlap_check(blob1,blob2,length):
    blob1_x = blob1[0].x()
    blob1_y = blob1[0].y()
    blob2_x = blob2[0].x()
    blob2_y = blob2[0].y()
    if blob1_y + length <= blob2_y:
        return True
    if blob1_y >= (blob2_y + length):
        return True
    if (blob1_x + length) <= blob2_x:
        return True
    if blob1_x >= (blob2_x + length):
        return True

    else:
        if blob1_x >= blob2_x:
            width = blob2_x + length - blob1_x
        else:
            width = blob1_x + length - blob2_x
        if blob1_y >= blob2_y:
            height = blob2_y + length - blob1_y
        else:
            height = blob1_y + length - blob2_y
        area = width * height
        print("overlap_area:"+str(area))
        if area <= 70:
            return True
        else:
            return False
def cal_piexl(input_img,input_threshold):
    blobs = input_img.find_blobs([(input_threshold,255)])
    pixels = 0
    for the_blob in blobs:
       pixels += the_blob.pixels()
    return pixels
def abnormal_threshold_check(last_img,realtime_img,last_threshold,realtime_threshold,consult_threshold,ratio,consult_thresholds):
    sub_threshold = realtime_threshold - consult_threshold
    print(str(sub_threshold))
    if abs(sub_threshold) <= 5:
        return realtime_threshold
    else:
        piexl_realtime= cal_piexl(realtime_img,realtime_threshold)
        if piexl_realtime >2000:
            return consult_threshold
        else:
            piexl_last= cal_piexl(last_img,last_threshold)
            if piexl_last:
                tmp_ratio = abs(piexl_last - piexl_realtime)/piexl_last
                print("piexl_last: "+str(piexl_last))
                print("piexl_realtime: "+str(piexl_realtime))
                print("ratio: "+str(tmp_ratio))
                if tmp_ratio <= ratio:
                    consult_threshold = control_oscillations(consult_thresholds,realtime_threshold,100)
                    return realtime_threshold
                else:
                    return consult_threshold
            else:
                return consult_threshold

#def pixel_check(input_img,input_threshold,number,crosser_type):
    #pixel = cal_piexl(input_img,input_threshold)
    #if crosser_type == 1:
        #if pixel <= value1:
            #return True
        #else:
            #return False
    #elif crosser_type == 2:
        #if pixel <= value2:
            #return True
        #else:
            #return False
    #elif crosser_type == 3:
        #if pixel <= value3:
            #return True
        #else:
            #return False
    #else:
        #return False





uart = UART(3, 115200)
count1 = 0
count2 = 0
count3 = 0
count_sampling = 0
count_croesser = 0
theta = None
rho = None
intersection = None
thetas = []
rhos = []
last_threshold = 0
consult_gray_threshold = 0
consult_gray_thresholds = []
last_list =[0,40,0]
extra_list = [0,40,0]
mask_none = False
mask_threshold = False
mask_croesser = False
output_str = None
last_img = sensor.snapshot()
while(True):
    clock.tick()
    #led_B.off()
    #led_G.off()
    src_img = sensor.snapshot()
    corr_img = src_img
    corr_img =src_img.lens_corr(1.5)
    #corr_img.mean(1)
    tmp_histogram = corr_img.get_histogram()
    #realtime_gray_threshold = tmp_histogram.get_threshold().value()
    realtime_gray_threshold = tmp_histogram.get_statistics().mean()
    if mask_threshold:
        gray_threshold_low = abnormal_threshold_check(last_img,corr_img,last_threshold,realtime_gray_threshold,consult_gray_threshold,0.5,consult_gray_thresholds)
    else:
        count_sampling += 1
        tmp_value = control_oscillations(consult_gray_thresholds,realtime_gray_threshold,100)
        gray_threshold_low = realtime_gray_threshold
        if count_sampling >= 120:
            consult_gray_threshold = tmp_value
            mask_threshold = True
    last_img = corr_img.copy()
    last_threshold = gray_threshold_low
    gray_threshold = [(gray_threshold_low+23,255)]
    print("consult_gray_threshold:"+str(consult_gray_threshold))
    print("threshold:"+str(gray_threshold))
    lines = corr_img.find_lines((0,0,80,60),2,1,300)
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
                        if abs(line1.rho() - last_list[1]) > abs(line2.rho() - last_list[1]):
                            del lines[ii]
                        else:
                            del lines[jj+ii+1]
        print("length: "+str(len(lines)))
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
                #print("sub"+str(sub))
                if 70<=sub<=105 or 30<=sub<=50 or 120<=sub<=140:
                    ##fine crossover point
                    corr_img.draw_line(line1.line(),50)
                    corr_img.draw_line(line2.line(),50)
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
                        if overlap_check(blobs[0],blobs[4],10):
                            mid_x1 = (crossover_x + points1[0][0])/2
                            mid_y1 = (crossover_y + points1[0][1])/2
                            count1 +=1
                    if blobs[1] and blobs[5]:
                        if overlap_check(blobs[1],blobs[5],10):
                            mid_x1 = (crossover_x + points1[1][0])/2
                            mid_y1 = (crossover_y + points1[1][1])/2
                            count1 +=1
                    # discriminate seacon line
                    if blobs[2] and blobs[6]:
                        if overlap_check(blobs[2],blobs[6],10):
                            mid_x2 = (crossover_x + points2[0][0])/2
                            mid_y2 = (crossover_y + points2[0][1])/2
                            count2 +=1
                    if blobs[3] and blobs[7]:
                        if overlap_check(blobs[3],blobs[7],10):
                            mid_x2 = (crossover_x + points2[1][0])/2
                            mid_y2 = (crossover_y + points2[1][1])/2
                            count2 +=1
                    print("count1: "+str(count1))
                    print("count2: "+str(count2))

                    #discriminate intersection
                    if (count1+count2)==2:
                        #"7"">"
                        if count1==1 and count2==1:
                            if 70<=sub<=105:
                                intersection = 2
                            if 30<=sub<=50 or 120<=sub<=140:
                                intersection = 4
                            dst_x1 = round(mid_x1)
                            dst_y1 = round(mid_y1)
                            dst_x2 = round(mid_x2)
                            dst_y2 = round(mid_y2)
                            points = [[dst_x1,dst_y1],[dst_x2,dst_y2]]
                            corr_img.draw_line((dst_x1,dst_y1,dst_x2,dst_y2),50)
                            para = get_para_of_line(points)
                            theta = round(para[0])
                            if theta > 90:
                                theta -= 180
                            rho = round(para[1])
                            #filter
                            theta = control_oscillations(thetas,theta,20)
                            rho = control_oscillations(rhos,rho,50)
                            output_list = [theta,rho,intersection]
                            mask_none = True
                    elif (count1+count2)==4:
                        intersection = 3
                        output_list = [999,999,intersection]
                        mask_none = True
                        thetas.clear()
                        rhos.clear()
                    else:
                        #print("can't identify right croesser")
                        mask_none = False
                        output_list = last_list
                    count1 = 0
                    count2 = 0
                else:
                    #print("no right angle lines")
                    mask_none = False
                    output_list = last_list
        if not mask_none:
            #print("d")
            true_lines = []
            if last_list[2] == 3:
                last_theta = extra_list[0]
            else:
                last_theta = last_list[0]
            for the_line in lines:
                crossover_point = [(the_line.x1() + the_line.x2())/2,(the_line.y1() + the_line.y2())/2]
                point_t = [the_line.x1(),the_line.y1()]
                point_b = [the_line.x2(),the_line.y2()]
                blobs = []
                blobs_t_c = range_check(corr_img,gray_threshold,crossover_point,point_t,0.35)
                blobs_t_f = range_check(corr_img,gray_threshold,crossover_point,point_t,0.9)
                blobs_b_c = range_check(corr_img,gray_threshold,crossover_point,point_b,0.35)
                blobs_b_f = range_check(corr_img,gray_threshold,crossover_point,point_b,0.9)
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
                #print("count3:"+str(count3))
                if count3 >= 3:
                    tmp_theta = the_line.theta()
                    if tmp_theta > 90:
                        tmp_theta -= 180
                    if abs(tmp_theta - last_list[0]) <= 50:
                        true_lines.append(the_line)
                count3 = 0
            if true_lines:
                #print("len:"+str(len(true_lines)))
                if len(true_lines) > 1:
                    sum_theta = 0
                    sum_rho = 0
                    for the_line in true_lines:
                        tmp_theta = the_line.theta()
                        if tmp_theta > 90:
                            tmp_theta -= 180
                        sum_theta += tmp_theta
                        if tmp_theta > 0:
                            sum_rho += the_line.rho()
                        else:
                            points = [[the_line.x1(),the_line.y1()],[the_line.x2(),the_line.y2()]]
                            crossover_point = get_crosser_point(points,False)
                            sum_rho += get_rho(crossover_point)
                        #corr_img.draw_line(the_line.line())
                    theta = round(sum_theta/len(lines))
                    rho = round(sum_rho/len(lines))
                else:
                    #corr_img.draw_line(true_lines[0].line())
                    tmp_theta = true_lines[0].theta()
                    if tmp_theta > 90:
                        tmp_theta -= 180
                    theta = tmp_theta
                    if theta > 0:
                        rho = true_lines[0].rho()
                    else:
                        points = [[true_lines[0].x1(),true_lines[0].y1()],[true_lines[0].x2(),true_lines[0].y2()]]
                        crossover_point = get_crosser_point(points,False)
                        rho = get_rho(crossover_point)
                #print("theta:"+str(theta))
                #print("rho:"+str(rho))

                theta = control_oscillations(thetas,theta,20)
                rho = control_oscillations(rhos,rho,50)
                intersection = 1
                output_list = [theta,rho,intersection]
                mask_none = True
            else:
                #print("no right lines")
                mask_none = False
                output_list = last_list

    else:
        #print("no lines")
        mask_none = False
        output_list = last_list

    #print (output_list)
    if mask_none:
        if output_list[2] == 3:
            extra_list = last_list
        last_list = output_list


    #if output_list[2] !=3:
        #if abs(output_list[0]) < 10:
            #if output_list[0] >= 0:
                #str_theta = "10%d" % (output_list[0])
            #else:
                #str_theta = "00%d" % (-output_list[0])
        #else:
            #if output_list[0] >= 0:
                #str_theta = "1%d" % (output_list[0])
            #else:
                #str_theta = "0%d" % (-output_list[0])

        #if output_list[1]//100 == 0:
            #if output_list[1]//10 == 0:
                #str_rho = "00%d" % (output_list[1])
            #else:
                #str_rho = "0%d" % (output_list[1])
        #else:
            #str_rho = "%d" % (output_list[1])
        #str_intersection = str(output_list[2])
        #output_str = "$"+str_theta+","+str_rho+","+str_intersection
    #else:
        #output_str = "$999,999,3"
    print(output_list)
    if output_list[2] == 1:
        if output_list[0] > 5:
            output_str = "5"
        if -5 <= output_list[0] <= 5:
            output_str = "7"
        if output_list[0] < -5:
            output_str = "6"

    if output_list[2] == 4:
        output_str = "2"
    if output_list[2] == 2:
        if output_list[1] >= 40:
            output_str = "3"
    print(output_str)
    count1 = 0
    count2 = 0
    count3 = 0
    mask_none = False
    if output_str:
        if (output_str == "5") or (output_str == "6"):
            led_B.off()
            led_G.off()
            led_R.off()
            led_G.on()
            led_R.on()
        elif output_str == "2":
            led_B.off()
            led_G.off()
            led_R.off()
            led_B.on()
            led_G.on()
        elif output_str == "3":
            led_B.off()
            led_G.off()
            led_R.off()
            led_B.on()
            led_R.on()
        elif output_str == "7":
            led_B.off()
            led_G.off()
            led_R.off()
            led_B.on()
            led_G.on()
            led_R.on()
        uart.write(output_str)
    #uart.write(output_str)
    output_str = None
    print(clock.fps())
    print(" ")




