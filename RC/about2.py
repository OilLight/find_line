# Untitled - By: oillight - 周六 4月 20 2019

import  image, math

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
    if tmp_x != 0:
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
    #img.draw_rectangle((input_x,input_y,input_w,input_h),127)
    return blobs

def overlap_check(blob1,blob2):
    if((blob1[0].y()+8)<blob2[0].y()) or (blob1[0].y()>(blob2[0].y()+8)) or ((blob1[0].x()+8)<blob2[0].x()) or (blob1[0].x()>(blob2[0].x()+8)):
        return True
    else:
        return False

