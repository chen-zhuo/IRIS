class MyDataType():
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
    
    def __str__(self):
        return str(self.data1) + ' ' + str(self.data2)

def func():
    x = 999

list1 = [1, 2, 3]
list2 = list1

list1 = ['a', 'b', 'c']

print(list1)
print(list2)

print('================================')

str1 = '123'
str2 = str1

str1 = 'abc'

print(str1)
print(str2)

print('================================')

myData1 = MyDataType(1, 2)
myData2 = MyDataType('aaa', 'bbb')
myData3= MyDataType(True, False)

list1 = [myData1, myData2, myData3]
list2 = list1

list1 = [myData3, myData2, myData1]

print(list1)
print(list2)


print('================================')

list1 = [1, 2, 3]
func(list1)
print(list1)














