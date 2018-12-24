import os
from vector import *
from PIL import Image




def get_imageset():
    imageset =[]
    for letter in os.listdir("iconset"):
        for ele in os.listdir("iconset/{}/".format(letter)):
            temp = []
            _file = "iconset/{}/{}".format(letter, ele)
            a = buildvector(Image.open(_file))
            if type(a[0])==tuple:
                #os.remove(_file)

                raise Exception("图片未二值化")
            if sum(a.values())==0:
                os.remove(_file)
                raise Exception("不合法 {}".format(_file))
            temp.append(buildvector(Image.open(_file)))
            imageset.append({letter: temp})
    return imageset

def recongize(crop_im ,imageset):
    guess = []
    v = VectorCompare()
    for image in imageset:
        for x, y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0] ,buildvector(crop_im)),x))
    guess.sort(reverse=True)
    print(guess[0] )
    return guess[0][1]


