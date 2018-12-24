def depoint(img, threshold):
    """传入二值化后的图片进行降噪"""
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):

            #边界直接为空白
            if x ==0 or y ==0 or x ==w-1 or y == h-1:
                pixdata[x,y] =255
                continue
            count = 0
            if pixdata[x, y - 1] > threshold:  # 上
                count = count + 1
            if pixdata[x, y + 1] > threshold:  # 下
                count = count + 1
            if pixdata[x - 1, y] > threshold:  # 左
                count = count + 1
            if pixdata[x + 1, y] > threshold:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > threshold:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > threshold:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > threshold:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > threshold:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img