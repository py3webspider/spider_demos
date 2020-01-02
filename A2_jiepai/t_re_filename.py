# coding: utf-8
"""
@author: Evan
@time: 2019/12/31 16:32
"""
import re

filename = 'xxx\/:*?"<>|\/yyy'
filename = re.sub('[/:*?"<>|\\\]', '', filename)
print(filename)

