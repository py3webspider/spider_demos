# coding: utf-8
"""
@author: Evan
@time: 2020/1/7 17:27
"""
import tesserocr
from PIL import Image

image = Image.open('code2.jpg')

# 灰度处理与二值化处理
image = image.convert('L')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
result = tesserocr.image_to_text(image)
print(result)
