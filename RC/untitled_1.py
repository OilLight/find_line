# Untitled - By: oillight - 周三 5月 1 2019

import sensor, image, time



class my_line():
    def _init_(self,theta,rho):
        self.thate = theta
        self.rho = rho
        self.points = cal_points()
    def get_thate(self):
        return self.theta
    def get_rho(self):
        return self.theta
    def get_points(self):
        return self.points
    def cal_points():
        theta = self.theta
        rho = self.rho
        point1 = []
        point2 = []
        tmp_points = []
        value_sin = sin(theta)
        value_cos = cos(rho)
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
                tmp_points.append(x1)
                tmp_points.append(x1)
            y = (rho - 79 * value_cos) / value_sin
            if y>= 0:
                y3 = y
                x3 = 79
                tmp_points.append(x1)
                tmp_points.append(x1)
            x = rho/value_cos
            if x>= 0:
                x3 = x
                y3 = 0
                tmp_points.append(x3)
                tmp_points.append(x3)
            x = (rho - 59 * value_sin) / value_cos
            if x>= 0:
                x3 = x
                y3 = 59
                tmp_points.append(x3)
                tmp_points.append(x3)
        output_points = [[tmp_points[0],tmp_points[1]],[tmp_points[2],tmp_points[3]]]
        return output_points
    def change_param(self,thate,rho):
        self.thate = thate
        self.rho = rho
        self.cal_points()

    def line_merge(my_line)




sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
