import pandas
import random


columns = ["a", "b", "c"]
cols = []
for i in range(3):
    cols.append(int(random.random()*100))
print(cols)

print("*"*100)
df = pandas.DataFrame(columns=columns)
for i in range(3):
    df.insert(1, i, cols)  # 意思是插入列的意思
print(df)

print("*"*100)
df = pandas.DataFrame(columns=columns)
df.set_value(0, "a", columns)  # 插入指定位置的一个值
df.set_value(2, "b", 5)
print(df)
