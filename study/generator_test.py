#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Fib(object):

    def __init__(self, max):
        print('init:', max)
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def next(self):
        print('next max:{} n:{} a:{} b:{}'.format(self.max, self.n, self.a, self.b))

        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()


# for n in Fib(5):
#     print(n)

print('-----------------------------')


def my_fibs(max):
    n, a, b = 0, 0, 1
    while n < max:
        # print('my_fibs')
        yield b  # 使用 yield生成生成生成器,yield就是 return 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后开始
        a, b = b, a + b
        n = n + 1
        # print(n, b)


print(my_fibs(10))
print(next(my_fibs(10)))
print('-----------------------------')

for n in my_fibs(5):
    print('n', n)

L = [x * 2 for x in range(5)]
print(L)  # [0, 2, 4, 6, 8]

print('-----------------------------')

G = (x * 2 for x in range(5))  # 生成器
print(G)  # <generator object <genexpr> at 0x10fb86a50>
print(next(G))  # 0
print(next(G))  # 2

print('-----------------------------')

# 用生成器函数生成list
l1 = list(my_fibs(10))
print(l1)
