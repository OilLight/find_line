# about - By: oillight - 周二 4月 9 2019

import image

def find_biggest_blob(blobs):
    biggest = 0
    the_max = 0
    for i in range(len(blobs)):
        if temp_blobs[i][4] > biggist:
            biggist = temp_blobs[i][4]
            the_max = i

    biggest_blob = temp_blobs[the_max]
    return biggest_blob



def judge_line(blobs):
    judge = False
    while blobs:
        tmp_blob = fine_biggest_blob(blobs)
        if tmp_blob.pixels() <= 40:
            judge = True
            break
        else:
            tmp_blob.pop(tmp_blob)

    return judge



def lanes_identificate(img,the_threshold,height,distance):
    #lanes identification
    count = 0
    lanes = 0

    top_blobs = tmp_img.find_blobs(the_threshold,False,(distance+height,distance,80-(2*(height+distance)),height),2,1)
    if top_blobs:
        #print('top')
        if judge_line(top_blobs):
            count += 1

    left_blobs = tmp_img.find_blobs(the_threshold,False,(distance,distance+height,height,60-(2*(height+distance))),2,1)
    if left_blobs:
        #print('left')
        if judge_line(left_blobs):
            count += 1

    bottom_blobs = tmp_img.find_blobs(the_threshold,False,(distance+height,59-distance-height,80-(2*(height+distance)),height),2,1)
    if bottom_blobs:
        #print('bottom')
        if judge_line(bottom_blobs):
            count += 1

    right_blobs = tmp_img.find_blobs(the_threshold,False,(79-distance-height,distance+height,height,60-(2*(height+distance))),2,1)
    if right_blobs:
        #print('right')
        if judge_line(right_blobs):
            count += 1

    if count == 2:
        if (top_blobs and bottom_blobs) or (right_blobs and left_blobs):
            lanes = 1
        elif (top_blobs and right_blobs) or (top_blobs and left_blobs) or (bottom_blobs and right_blobs) or (bottom_blobs and left_blobs):
            lanes = 2

    elif count == 3:
        lines = img.fine_line()
        for i in len(lines)
            for j in len(lines)
                if (j+i) >= len(lines):
                    break
                theta1 = lines[i].theta()
                theta2 = lines[j+i].theta()
                if 70 < abs(theta1 - theta2) < 105:
                    lanes = 2
                    break
            if lanes:
                break

    elif count == 4:
        lanes = 3

    return lanes



def get_average(data):
    average = sum(data) / len(tmps)
    average = round(average)
    return average



def filter(data):
    length = len(data)

    if length >2:
        sorted(data)
        tmps = data[1:length]
    average = get_average(tmps)

    return average



def control_oscillations(data,datum,length):
    if (len(data) >= length):
        del data[0]
    data.append(datum)
    output_value = filter(data)

def highlight_check_one(img,the_blob,the_threshold,n,ratio):
    tmp = floor(the_blob.h() / n)
    tmp_blobs = []
    for i in range(n)
        roi = (the_blob.x(),i*tmp,the_blob.w(),tmp)
        tmp_blobs = tmp_img.find_blobs(the_threshold,False,roi,2,1,10,10,True)
        tmp_blob = find_biggest_blob(tmp_blobs)
        tmp_pixels.append(tmp_blob[4])
    average = get_average(tmp_pixels)

    for j in range(n):
        tmp = tmp_pixels[j] / average
        if tmp > ratio:
            #tmp_img = img.copy()
            #tmp_img.clear()
            #for y in range(tmp):
                #for x in range(the_blob.w()):
                    #tmp_img.set_pixel(x+the_blob.x(),y+j*tmp,255)
            #tmp_img.invert()
            #img.b_and(tmp_img)

            for y in range(tmp):
                for x in range(the_blob.w())
                    img.set_pixel(x+the_blob.x(),y+j*tmp,0)


