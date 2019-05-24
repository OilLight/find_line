# Untitled - By: oillight - 周四 4月 25 2019
import sensor, image, time, math
from pyb import UART
sensor.reset()
#sensor.set_auto_exposure(False, 800)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()


class my_line():
    def _init_(self,input_points = None,input_theta = None,input_rho = None,input_line = None):
        if input_points:
            self.points = input_points
            if input_theta and  input_rho :
                self.thate = input_theta
                self.rho = input_rho
            else:
                param = self.cal_para_of_line()
                self.thate = param[0]
                self.rho = param[1]
        else:
            self.thate = input_line.theta()
            self.rho = input_line.rho()
            self.points = [[input_line.x1(),input_line.y1()],[input_line.x2(),input_line.y2()]]
    def get_thate(self):
        return self.theta
    def get_rho(self):
        return self.theta
    def get_points(self):
        return self.points

    def cal_rho(self,point):
        origin_point = [0,0]
        rho = find_distance(point,origin_point)
        return rho

    def cal_theta(self,point):
        theta = math.atan2(point[1], point[0])*180/math.pi
        if theta<0:
            theta += 180
        return theta

    def cal_points():
        theta = self.theta
        rho = self.rho
        point1 = []
        point2 = []
        tmp_points = []
        value_sin = sin(theta)
        value_cos = cos(theta)
        if value_sin == 0:
            x1 = rho
            x2 = rho
            y1 = 0
            y2 = 59
            self.points = [[x1,y1],[x2,y2]]
        elif not value_cos == 0:
            y1 = rho
            y2 = rho
            x1 = 0
            x2 = 79
            self.points = [[x1,y1],[x2,y2]]
        else:
            y = rho / value_sin
            if y>= 0:
                y3 = y
                x3 = 0
                tmp_points.append(x3)
                tmp_points.append(y3)
            y = (rho - 79 * value_cos) / value_sin
            if y>= 0:
                y3 = y
                x3 = 79
                tmp_points.append(x3)
                tmp_points.append(y3)
            x = rho/value_cos
            if x>= 0:
                x3 = x
                y3 = 0
                tmp_points.append(x3)
                tmp_points.append(y3)
            x = (rho - 59 * value_sin) / value_cos
            if x>= 0:
                x3 = x
                y3 = 59
                tmp_points.append(x3)
                tmp_points.append(y3)
        output_points = [[tmp_points[0],tmp_points[1]],[tmp_points[2],tmp_points[3]]]
        return output_points

    def find_equation(self,input_points=[]):
        if input_points:
            point1 = input_points[0]
            point2 = input_points[1]
        else;
            point1 = self.points[0]
            point2 = self.points[1]
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

    def get_crosser_point(self, mask=True, points1=self.points, points2=[]):
        crossover_x = 0
        crossover_y = 0
        para1 = find_equation(points1)
        #print("para1:"+str(para1))
        if points2:
            para2 = self.find_equation(points2)
            if len(para1) == 2 and len(para2) == 2:z
                if para1[0] != para2[0]
                    crossover_x = (para2[1]-para1[1])/(para1[0]-para2[0])
                    crossover_y =  para1[0]*crossover_x+para1[1]
                else:
                    return None
            else:
                if len(para2) == 2:
                    crossover_x = para1[0]
                    crossover_y = para2[1]
                elif len(para1) == 2:
                    crossover_x = para2[0]
                    crossover_y = para1[1]
                else:
                    return None
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

    def cal_para_of_line(self):
        the_points = self.points
        tmp_y = the_points[0][1] - the_points[1][1]
        tmp_x = the_points[0][0] - the_points[1][0]
        if tmp_x !=0:
            k = tmp_y/tmp_x
            crossover_point = self.get_crosser_point()
            if k > 0:
                crossover_point_anti = self.get_crosser_point(False)
                rho = self.cal_rho(crossover_point_anti)
            else:
                rho = self.cal_rho(crossover_point)
            theta = self.cal_theta(crossover_point)
        else:
            rho = points[0][0]
            theta = 0
        para = [theta,rho]
        return para

    def line_merging(self,the_line):
        theta1 = self.get_theta()
        theta2 = the_line.get_theta()

        if theta1 <= 90 and theta2 <= 90:
            tmp_theta1 = theta1
            tmp_theta2 = theta2
        elif theta2 <= 90:
            tmp_theta1 = theta1 - 180
            tmp_theta2 = theta2
        elif theta1 <= 90:
            tmp_theta2 = theta2 - 180
            tmp_theta1 = theta1
        else:
            tmp_theta1 = theta1 - 180
            tmp_theta2 = theta2 - 180
        theta = (tmp_theta1 + tmp_theta2)/2

        if theta1 != theta2:
            crossover_point = get_crosser_point(True,self.points,the_line.get_points())
            if tmp_theta != 90
                tan_value = tan(tmp_theta)
                if tan_value != 0:
                    tmp_y = crossover_point[1]
                    x = crossover_point[0] + tmp_y / tan_value
                    tmp_points = [crossover_point,[x,0]]
                    crossover_point_for_rho = self.get_crosser_point(True,tmp_points)
                    rho = self.cal_rho(crossover_point_for_rho)
                else:
                    rho = crossover_point[0]
            else:
                rho = crossover_point[1]
        else:
            rho = (self.theta + the_line.get_theta())/2
        if rho < 0:
            rho += 180
        self.change_param(theta,rho)


    def change_param(self,thate,rho):
        self.thate = thate
        self.rho = rho
        self.cal_pointscal_points = self.cal_points()



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


def find_distance(point1, point2):
    distance = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    return distance

def range_check(img,threshoid,crosser_point, end_point, ratio, the_range=10):
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
count_sampling = 0
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
mask_threshold = True
output_str =" "
while(True):
    clock.tick()
    src_img = sensor.snapshot()
    corr_img =src_img.lens_corr(1.6)
    corr_img.mean(1)
    if mask_threshold:
        tmp_histogram = corr_img.get_histogram()
        tmp_threshold = tmp_histogram.get_threshold().value()
        gray_threshold = [(tmp_threshold,255)]
        mask_threshold = False
    print("threshold:"+str(gray_threshold))
    lines = src_img.find_lines((0,0,80,60),2,1,300)
    #for the_line in lines:
        #corr_img.draw_line(the_line.line())
        #print("("+str(the_line.x1())+","+str(the_line.y1())+") ("+str(the_line.x2())+","+str(the_line.y2())+")")
    if lines:
        my_lines = []
        for ii in range(len(lines)):
            for jj in range(len(lines)):
                if (jj+ii+1) >= len(lines):
                    break
                line1 = my_line(lines[ii].theta(),lines[ii].rho(),[[lines[ii].x1(),lines[ii].y1()],[lines[ii].x2(),lines[ii].y2()]])
                line2 = my_line(lines[jj+ii+1])(lines[jj+ii+1].theta(),lines[jj+ii+1].rho(),[[lines[jj+ii+1].x1(),lines[jj+ii+1].y1()],[lines[jj+ii+1].x2(),lines[jj+ii+1].y2()]])

                if abs(line1.get_theta()-line2.get_theta())<=10 and abs (line1.get_rho()-line2.get_rho())<=10:
                   line1.line_merging(line2)
                   my_lines.append(line1)
                else:
                    my_lines.append(line1)
                    my_lines.append(line2)
        #print("length: "+str(len(lines)))
        for i in range(len(my_lines)):
            if mask_none:
                break
            for j in range(len(my_lines)):
                if mask_none:
                    break
                if (j+i+1) >= len(my_lines):
                    break
                line1 = my_lines[i]
                line2 = my_lines[j+i+1]
                points1 = line1.get_points()
                points2 = line2.get_points()

                line1_point1 = points1[0]
                line1_point2 = points1[0]
                line2_point1 = points2[1]
                line2_point2 = points2[1]

                #exclude point
                if line1_point1 == line1_point2:
                    continue
                if line2_point1 == line2_point2:
                    continue
                #fine perpendicular lines or 45 degree angle
                theta1 = line1.get_theta()
                theta2 = line2.get_theta()
                sub = abs(theta1 - theta2)
                #print("sub"+str(sub))
                if 70<=sub<=105 or 30<=sub<=50 or 120<=sub<=140:
                    ##fine crossover point
                    corr_img.draw_line([line1_point1[0],line1_point1[1],line1_point2[0],line1_point2[1]],127)
                    corr_img.draw_line([line2_point1[0],line2_point1[1],line2_point2[0],line2_point2[1]],127)

                    points = [points1[0],points1[1],points2[0],points2[1]]
                    crossover_point = []
                    crossover_point = line1.get_crosser_point(True,points1,points2)
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
                    #print("count1:"+str(count1))
                    #print("count2:"+str(count2))
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
                            connecting_line = my_line(None,None,None,points)
                            theta = connecting_line.get_theta()
                            if theta > 90:
                                theta = 180 - theta
                            rho = connecting_line.get_rho()
                            #filter
                            theta = control_oscillations(thetas,theta,10)
                            rho = control_oscillations(rhos,rho,10)
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
                    count1 = 0
                    count2 = 0
                else:
                    #print("no right angle lines")
                    mask_none = False
                    output_list = last_list
        if not mask_none:
            #print("d")
            true_lines = []
            for the_line in my_lines:
                points = the_line.get_points()
                crossover_point = [(points[0][0]+ points[1][0])/2,(points[0][1] + points[1][1])/2]
                point_t = points[0]
                point_b = points[1]
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
                #print("count3:"+str(count3))
                if count3 >= 3:
                    true_lines.append(the_line)
                count3 = 0
            if true_lines:
                #print("len:"+str(len(true_lines)))
                if len(true_lines) > 1:
                    sum_theta = 0
                    sum_rho = 0
                    for the_line in true_lines:
                        tmp_theta = the_line.get_theta()
                        if tmp_theta > 90:
                            tmp_theta -= 180
                        sum_theta += tmp_theta
                        if tmp_theta > 0:
                            sum_rho += the_line.get_rho()
                        else:
                            crossover_point = true_lines.get_crosser_point(False,points)
                            sum_rho += get_rho(crossover_point)
                        #corr_img.draw_line(the_line.line())
                    theta = sum_theta/len(lines)
                    rho = sum_rho/len(lines)
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
                        crossover_point = get_crosser_point(False,points)
                        rho = get_rho(crossover_point)
                #print("theta:"+str(theta))
                #print("rho:"+str(rho))

                theta = control_oscillations(thetas,theta,10)
                rho = control_oscillations(rhos,rho,10)
                intersection = 1
                last = [theta,rho]
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
        last_list = output_list
    if output_list[2] !=3:
        if output_list[0]//10 == 0:
            if output_list[0] >= 0:
                str_theta = "10%d" % (output_list[0])
            else:
                str_theta = "00%d" % (-output_list[0])
        else:
            if output_list[0] >= 0:
                str_theta = "1%d" % (output_list[0])
            else:
                str_theta = "0%d" % (-output_list[0])

        if output_list[1]//100 == 0:
            if output_list[1]//10 == 0:
                str_rho = "00%d" % (output_list[1])
            else:
                str_rho = "0%d" % (output_list[1])
        else:
            str_rho = "%d" % (output_list[1])
        str_intersection = str(output_list[2])
        output_str = "$"+str_theta+","+str_rho+","+str_intersection
    else:
        output_str = "$999,999,3"

    print(output_str)
    count1 = 0
    count2 = 0
    count3 = 0
    mask_none = False
    uart.write(output_str)
    #print(clock.fps())
    print(" ")



