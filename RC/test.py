# Untitled - By: oillight - 周四 4月 18 2019

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

def find_equation(points):
    point1 = points[0]
    point2 = points[1]
    tmp_x = point1[0] - point2[0]
    tmp_y = point1[1] - point2[1]
    if tmp_x != 0:
        k = tmp_y/tmp_x
        b = point1[1] - k*point1[0]
        output_list = [k,b]
    else:
        x = points[0]
        output_list = [x]
    return output_list

def get_crosser_point(points1 ,mask=True, points2=[]):
    crossover_x = 0
    crossover_y = 0
    para1 = find_equation(points1)
    print(para1)
    if points2:
        para2 = find_equation(points2)
        if len(para1) == 2 and len(para2) == 2:
            crossover_x = (para2[1]-para1[1])/(para1[0]-para2[0])
            crossover_y =  k*crossover_x+b
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
    crossover_point = [crossover_x,crossover_y]
    return crossover_point


while(True):
    clock.tick()
    img = sensor.snapshot()

    point1 = [35,20]
    point2 = [50,40]
    point3 = [40,30]
    point4 = [10,48]
    points1 = [point1,point2]
    points2 = [point3,point4]
    crossover_point = get_crosser_point(points1,False)
    print(crossover_point)
    img.draw_line(point1[0],point1[1],point2[0],point2[1])
    img.draw_line(int(crossover_point[0]),int(crossover_point[1]),79,0)
    print(clock.fps())
