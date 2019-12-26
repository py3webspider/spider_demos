# coding: utf-8
"""
@author: Evan
@time: 2019/12/26 18:24

1. pip install -i https://pypi.douban.com/simple pymongo

参考文档：
[Python3网络爬虫开发实战] 5.3.1-MongoDB存储
"""
# 2. 连接mongodb
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

# 3. 指定数据库
db = client.test

# 4. 指定集合
collection = db.students

# 5. 插入数据
student = {
    'id': '201314',
    'name': 'Evan',
    'age': 21,
    'gender': 'male'
}

result = collection.insert_one(student)
print(result)

student1 = {'id': '20170101', 'name': 'Jordan', 'age': 20, 'gender': 'male'}

student2 = {'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}

result = collection.insert_many([student1, student2])
print(result)
print(result.inserted_ids)


# 6. 查询
result = collection.find_one({'name': 'Evan'})
# print(type(result))  # <class 'dict'> 字典类型
# print(result)


results_ = collection.find({'name': 'Evan'})
# print(type(result))  # <class 'pymongo.cursor.Cursor'> 游标类型
# for result in results_:
#     print(result)


# 如果要查询年龄大于20的数据，则写法如下：
"""
$lt    小于
$gt    大于
$lte   小于等于
$gte   大于等于
$ne    不等于
$in    在范围内      {'age': {'$in': [20, 23]}}
$nin   不在范围内    {'age': {'$nin': [20, 23]}}
"""
results = collection.find({'age': {'$gt': 20}})
print(type(results))  # <class 'pymongo.cursor.Cursor'>
for result in results:
    print(result)

# 另外，还可以进行正则匹配查询。例如，查询名字以M开头的学生数据，示例如下
results_x = collection.find({'name': {'$regex': '^M.*'}})
"""
$regex  匹配正则表达式 {'name': {'$regex': '^M.*'}}      name以M开头
$exists 属性是否存在   {'name': {'$exists': True}}       name属性存在
$type   类型判断       {'age': {'$type': 'int'}}        age的类型为int
$mod    数字模操作     {'age': {'$mod': [5, 0]}}        年龄模5余0
$text   文本查询       {'$text': {'$search': 'Mike'}}  text类型的属性中包含Mike字符串
$where  高级条件查询   {'$where': 'obj.fans_count == obj.follows_count'}  自身粉丝数等于关注数
"""


# 7. 计数
# count = collection.find().count()
# output: DeprecationWarning: count is deprecated. Use Collection.count_documents instead.
count = collection.estimated_document_count()
print(count)

# 带条件的计数
db_count = collection.count_documents({'name': 'Evan'})
print(db_count)


# 8. 排序
# 升序 pymongo.ASCENDING
# 降序 pymongo.DESCENDING
sort = collection.find().sort('name', pymongo.DESCENDING)
print([s['name'] for s in sort])


# 9. 偏移
# 在某些情况下，我们可能想只取某几个元素，这时可以利用skip()方法偏移几个位置，
# 比如偏移2，就忽略前两个元素，得到第三个及以后的元素：
skip = collection.find().sort('name', pymongo.ASCENDING).skip(2)
print([sk['name'] for sk in skip])

# 另外，还可以用limit()方法指定要取的结果个数，示例如下：
skips = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)
print([sk['name'] for sk in skips])

# 值得注意的是，在数据库数量非常庞大的时候，如千万、亿级别，最好不要使用大的偏移量来查询数据，
# 因为这样很可能导致内存溢出。此时可以使用类似如下操作来查询：
from bson.objectid import ObjectId
obj = collection.find({'_id': {'$gte': ObjectId('5e048ce1e9b50a3686c41e74')}})
print([n['name'] for n in obj])


# 10. 更新
condition = {'name': 'Evan'}
student = collection.find_one(condition)
student['name'] = 'Evan'
student['gender'] = 'male'

# # DeprecationWarning: update is deprecated. Use replace_one, update_one or update_many instead.
# result = collection.update(condition, student)
# print(result)  # {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}

# result = collection.replace_one(condition, student)
# print(result)  # <pymongo.results.UpdateResult object at 0x0000021B02FEF708>

# # 如果不用$set的话，则会把之前的数据全部用student字典替换；如果原本存在其他字段，则会被删除。??
# result = collection.update(condition, {'$set': student})
# print(result)

results = collection.find({'age': {'$gte': 18}})
print(type(results))  # <class 'pymongo.cursor.Cursor'>
for result in results:
    print(result)

# 另外，update()方法其实也是官方不推荐使用的方法。这里也分为update_one()方法和update_many()方法，
# 用法更加严格，它们的第二个参数需要使用$类型操作符作为字典的键名，示例如下：
condition = {'name': 'Evan'}
student = collection.find_one(condition)
student['age'] = 18
result = collection.update_one(condition, {'$set': student})
print(result)
# 匹配的数据条数和影响的数据条数
print(result.matched_count, result.modified_count)

# 这里指定查询条件为年龄小于20，然后更新条件为{'$inc': {'age': 1}}，也就是年龄加1，
# 执行之后会将第一条符合条件的数据年龄加1
condition = {'age': {'$lt': 20}}
result = collection.update_one(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)
# <pymongo.results.UpdateResult object at 0x0000023006243608>
# 1 1


# 如果调用update_many()方法，则会将所有符合条件的数据都更新，示例如下：
condition = {'age': {'$gt': 20}}
result = collection.update_many(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)
# 这时匹配条数就不再为1条了，运行结果如下：
# >>> <pymongo.results.UpdateResult object at 0x0000012E10DD4A48>
# >>> 3 3
# 可以看到，这时所有匹配到的数据都会被更新。


# 11. 删除
# # DeprecationWarning: remove is deprecated. Use delete_one or delete_many instead.
# result = collection.remove({'name': 'Kevin'})
# print(result)

# 另外，这里依然存在两个新的推荐方法——delete_one()和delete_many()。示例如下：
result = collection.delete_one({'name': 'Tom'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$gt': 28}})
print(result.deleted_count)


# 12. 其他操作
"""
另外，PyMongo还提供了一些组合方法，如find_one_and_delete()、find_one_and_replace()和find_one_and_update()，
它们是查找后删除、替换和更新操作，其用法与上述方法基本一致。
另外，还可以对索引进行操作，相关方法有create_index()、create_indexes()和drop_index()等。
关于PyMongo的详细用法，可以参见官方文档：http://api.mongodb.com/python/current/api/pymongo/collection.html。

另外，还有对数据库和集合本身等的一些操作，这里不再一一讲解，
可以参见官方文档：http://api.mongodb.com/python/current/api/pymongo/。

本节讲解了使用PyMongo操作MongoDB进行数据增删改查的方法，后面我们会在实战案例中应用这些操作进行数据存储。

转载请注明：静觅 » [Python3网络爬虫开发实战] 5.3.1-MongoDB存储(https://cuiqingcai.com/5584.html)
"""



