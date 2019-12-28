# coding: utf-8
"""
@author: Evan
@time: 2019/12/28 14:08
"""
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

# 3. 指定数据库
db = client.weibo

# 4. 指定集合
collection = db.weibo

# 5. 查询所有
results_ = collection.find()
print(type(results_))  # <class 'pymongo.cursor.Cursor'> 游标类型
for result in results_:
    print(result)
