# coding: utf-8
"""
@author: Evan
@time: 2019/12/27 9:25
1. 准备工作：安装 redis 服务; pip install redis; 安装 Ruby; Ruby 下安装 redis-dump;
2. RedisPy 库提供两个类 Redis 和 StrictRedis 来实现 Redis 的命令操作
"""
from redis import StrictRedis, ConnectionPool

# 3. 连接Redis
# redis = StrictRedis(host='localhost', port=6379, db=0, password='123456')
# redis.set('name', 'Evan')
# print(redis.get('name'))     # b'Evan'
# # redis.exceptions.AuthenticationError: Authentication required.
#

# url 连接方式
url = 'redis://:123456@localhost:6379/0'
pool = ConnectionPool.from_url(url)
redis = StrictRedis(connection_pool=pool)
redis.set('Eva', 'Kevin')
print(redis.get('Eva'))

