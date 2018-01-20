from django.shortcuts import  HttpResponse
from PIL import Image, ImageDraw,  ImageFont
import random
import string
from io import BytesIO


# 生成随机字符串
def getRandomChar():
    # string模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.digits
    char = ''
    for i in range(4):
        char += random.choice(ran)
    return char


# 返回一个随机的RGB颜色
def getRandomColor():
    return (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120, 30), getRandomColor())
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体, ubuntu 字体在/usr/share/fonts/truetype/freefont
    # Wind字体放在C:\Windows\Fonts， 使用的是bahnschrift.ttf
    font = ImageFont.truetype('bahnschrift.ttf', 25)
    # 生成字符串

    code = getRandomChar()
    # 将生成的字符画在画布上
    for t in range(4):
        # 在画布上写字符串， 随机颜色
        draw.text((30 * t + 5, 0), code[t], getRandomColor(), font)

    # 生成干扰点
    for _ in range(random.randint(0, 50)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=getRandomColor())

    return img, code



