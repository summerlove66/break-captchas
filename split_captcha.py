from itertools import groupby
from queue import Queue
from PIL import Image



# drop shadow algorithm
def get_shadow_cutting_list(im):  #已经二值化过
    inletter = False
    foundletter = False

    letters =[]
    w, h = im.size
    pixdata = im.load()
    for x in range(1,w):
        for y in range(1,h):
            if pixdata[x,y] !=255:
                inletter =True

        if inletter and not foundletter:
            foundletter = True
            start = x
        if foundletter and  not inletter:
            foundletter = False
            end = x
            if end -start >2:
                letters.append((start,end))

        inletter = False

    return letters

def get_horizontal_range(im):  #竖直方向的切割。
    inletter = False
    foundletter = False
    vertical_range = []
    w, h = im.size
    start =0
    pixdata = im.load()
    for y in range(1, h):
        for x in range(1, w):
            if pixdata[x, y] != 255:
                inletter = True

        if inletter and not foundletter:
            foundletter = True
            start = y
        if foundletter and not inletter:
            foundletter = False
            end = y
            if end - start > 1:
                vertical_range = [start,end]
                break
        inletter = False

    return vertical_range



def get_cfs_cutting_list(im):
    pixdata = im.load()
    w, h = im.size
    visited = set()
    q = Queue()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []
    for x in range(w):
        for y in range(h):
            x_axis = []
            # y_axis = []
            if pixdata[x, y] == 0 and (x, y) not in visited:
                q.put((x, y))
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    try:
                        if pixdata[x_c, y_c] == 0:
                            q.put((x_c, y_c))
                            x_axis.append(x_c)
                            # y_axis.append(y_c)
                    except:
                        pass
            if x_axis:
               # print(x_axis)
                min_x, max_x = min(x_axis), max(x_axis)
                if max_x - min_x >2:
                    # 宽度小于3的认为是噪点，根据需要修改
                    cuts.append((min_x, max_x))
    return cuts


def vertical(im):
 """传入二值化后的图片进行垂直投影"""
 pixdata = im.load()
 w,h = im.size
 result = []
 for x in range(w):
  black = 0
  for y in range(h):
   if pixdata[x,y] == 0:
    black += 1
  result.append(black)
 return result


def get_start_x(hist_width):
 """根据图片垂直投影的结果来确定起点
  hist_width中间值 前后取4个值 再这范围内取最小值
 """
 mid = len(hist_width) // 2 # 注意py3 除法和py2不同
 temp = hist_width[mid-4:mid+5]
 return mid - 4 + temp.index(min(temp))


def get_nearby_pix_value(img_pix,x,y,j):

    """获取临近5个点像素数据"""
    offset = [ (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for x_offset ,y_offset  in offset:
        try:
            return 0 if img_pix[x+x_offset,y+y_offset] == 0 else 1

        except Exception:
                raise Exception("get_nearby_pix_value error")


def get_end_route(img, start_x, height):
    """获取滴水路径"""
    left_limit = 0
    right_limit = img.size[0] - 1
    end_route = []
    cur_p = (start_x, 0)
    last_p = cur_p
    end_route.append(cur_p)

    while cur_p[1] < (height - 1):
        sum_n = 0
        max_w = 0
        next_x = cur_p[0]
        next_y = cur_p[1]
        pix_img = img.load()
        for i in range(1, 6):
            cur_w = get_nearby_pix_value(pix_img, cur_p[0], cur_p[1], i) * (6 - i)
            sum_n += cur_w
            if max_w < cur_w:
                max_w = cur_w
        if sum_n == 0:
            # 如果全黑则看惯性
            max_w = 4
        if sum_n == 15:
            max_w = 6

        if max_w == 1:
            next_x = cur_p[0] - 1
            next_y = cur_p[1]
        elif max_w == 2:
            next_x = cur_p[0] + 1
            next_y = cur_p[1]
        elif max_w == 3:
            next_x = cur_p[0] + 1
            next_y = cur_p[1] + 1
        elif max_w == 5:
            next_x = cur_p[0] - 1
            next_y = cur_p[1] + 1
        elif max_w == 6:
            next_x = cur_p[0]
            next_y = cur_p[1] + 1
        elif max_w == 4:
            if next_x > cur_p[0]:
                # 向右
                next_x = cur_p[0] + 1
                next_y = cur_p[1] + 1
            if next_x < cur_p[0]:
                next_x = cur_p[0]
                next_y = cur_p[1] + 1
            if sum_n == 0:
                next_x = cur_p[0]
                next_y = cur_p[1] + 1
        else:
            raise Exception("get end route error")

        if last_p[0] == next_x and last_p[1] == next_y:
            if next_x < cur_p[0]:
                max_w = 5
                next_x = cur_p[0] + 1
                next_y = cur_p[1] + 1
            else:
                max_w = 3
                next_x = cur_p[0] - 1
                next_y = cur_p[1] + 1
        last_p = cur_p

        if next_x > right_limit:
            next_x = right_limit
            next_y = cur_p[1] + 1
        if next_x < left_limit:
            next_x = left_limit
            next_y = cur_p[1] + 1
        cur_p = (next_x, next_y)
        end_route.append(cur_p)
    return end_route


def get_split_seq(projection_x):
    split_seq = []
    start_x = 0
    length = 0
    for pos_x, val in enumerate(projection_x):
        if val == 0 and length == 0:
            continue
        elif val == 0 and length != 0:
            split_seq.append([start_x, length])
            length = 0
        elif val == 1:
            if length == 0:
                start_x = pos_x
            length += 1
        else:
            raise Exception('generating split sequence occurs error')
    # 循环结束时如果length不为0，说明还有一部分需要append
    if length != 0:
        split_seq.append([start_x, length])
    return split_seq


def do_split(source_image, starts, filter_ends):
    """
    具体实行切割
    : param starts: 每一行的起始点 tuple of list
    : param ends: 每一行的终止点
    """
    left = starts[0][0]
    top = starts[0][1]
    right = filter_ends[0][0]
    bottom = filter_ends[0][1]
    pixdata = source_image.load()
    for i in range(len(starts)):
        left = min(starts[i][0], left)
        top = min(starts[i][1], top)
        right = max(filter_ends[i][0], right)
        bottom = max(filter_ends[i][1], bottom)
    width = right - left + 1
    height = bottom - top + 1
    image = Image.new('L', (width, height), 255)
    for i in range(height):
        start = starts[i]
        end = filter_ends[i]
        for x in range(start[0], end[0] + 1):
            if pixdata[x, start[1]] == 0:
                image.putpixel((x - left, start[1] - top), 0)
    return image


def drop_fall(im):  #传入二值化后im
    sub_im_list =[ ]
    """滴水分割"""
    width, height = im.size
    # 1 二值化
    # 2 垂直投影
    hist_width = vertical(im)
    # 3 获取起点
    start_x = get_start_x(hist_width)

    # 4 开始滴水算法
    start_route = []
    for y in range(height):
        start_route.append((0, y))

    end_route = get_end_route(im, start_x, height)
    filter_end_route = [max(list(k)) for _, k in groupby(end_route, lambda x: x[1])]  # 注意这里groupby
    img1 = do_split(im, start_route, filter_end_route)

    sub_im_list.append(img1)
    start_route = list(map(lambda x: (x[0] + 1, x[1]), filter_end_route))  # python3中map不返回list需要自己转换
    end_route = []
    for y in range(height):
        end_route.append((width - 1, y))
    img2 = do_split(im, start_route, end_route)
    sub_im_list.append(img2)
    return sub_im_list


def split_letter(im,max_size):
    if im.size[0] <= max_size:
        return [im]
    split_im_list =[]

    for split_im in drop_fall(im):
        if split_im.size[0] <= max_size:
            split_im_list.append(split_im)
    return split_im_list

