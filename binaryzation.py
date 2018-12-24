def b_process(im ,threshold):
    im = im.convert("L")
    pixdata = im.load()
    w,h = im.size
    for  x  in range(w):
        for y in range(h):
            if pixdata[x,y] <threshold:
                pixdata[x,y] =0
            else:
                pixdata[x,y] =255
    return im
