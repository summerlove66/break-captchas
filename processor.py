import os
import uuid
from reduce_noise import depoint
from  binaryzation import b_process
from split_captcha import *
from recongize import recongize, get_imageset

BZ = 155 #  threshold of  binaryzation processing
RN = 240 # threshold of  noisy point reduction

MAX_LENGTH_CATCHA = 18  # if  the width of single letter over 17px  ,we gonna spilit it

IMAGE_SET = get_imageset() # load sample set


def process_one(img):
    im = depoint(b_process(Image.open(img), BZ), RN)
    letters = get_cfs_cutting_list(im)
    print(letters)
    letters.pop()
    for letter in letters:
        crop_im0 = im.crop((letter[0], 0, letter[1], im.size[1]))
        v_range = get_horizontal_range(crop_im0)
        crop_im = crop_im0.crop((0, v_range[0], letter[1] - letter[0], v_range[1]))
        for split_im in split_letter(crop_im, MAX_LENGTH_CATCHA):
            split_im =b_process(resize_img(split_im),BZ)
            yield split_im
    im.close()


def process_all(captcha_path):
    '''

    :param captcha_path: captchas sample directory which will be processed
    processing(binaryzation ,depoint ,resizing) the captchas .save the post-splited-captcha in  the elements directory
    '''
    i = 0
    for ele in os.listdir(captcha_path):
        _file = os.path.join(captcha_path, ele)
        for split_im in process_one(_file):
            split_im.save("elements\\{}".format(str(i) + "-" + ele))
            i += 1


def resize_img(im):
    return im.resize((MAX_LENGTH_CATCHA, MAX_LENGTH_CATCHA), Image.ANTIALIAS)



def recongize_img(img):
    '''

    :param img: the captcha  file which will be recongized
    :return: the result
    '''
    result = ""
    for split_im in process_one(img):
        result += recongize(split_im, IMAGE_SET).replace("x", "*")
    result = result[:-1] if not result[-1].isdigit() else result

    return eval(result)


if __name__ == '__main__':

    #process_all("captchas")
    for p in range(1,17):

        print(recongize_img("will_check\\download ({}).png".format(p)))