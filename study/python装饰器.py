import logging


# 普通装饰器
def use_logging(func):
    print('use_logging')

    def wrapper():
        logging.warning("%s is running" % func.__name__)
        # print("use_logging")
        return func()

    return wrapper


# 函数带参数的装饰器
def use_logging_with_param(func):
    print('use_logging_with_param')

    def wrapper(*args, **kwargs):
        # args是一个数组，kwargs一个字典
        logging.warning("%s is running" % func.__name__)
        # print("use_logging_with_param")
        return func(*args, **kwargs)

    return wrapper


# 带参数的装饰器
def use_logging_dynamic_level(level):
    print('use_logging_dynamic_level')

    def decorator(func):
        print(f'use_logging_dynamic_level decorator level({level})')

        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warning("%s is running" % func.__name__)
            elif level == "error":
                logging.error("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args)

        return wrapper

    return decorator


@use_logging
def foo():
    print("i am foo")


@use_logging_with_param
def square(width=0, height=0):
    print("i am square")
    print(f"{width} x {height} square is {width * height}")


@use_logging_dynamic_level(level="warn")
def bar(name='bar'):
    print("self is  %s" % name)


# 类装饰器
class obj_wrapper(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('class decorator runing')
        self._func()
        print('class decorator ending')


@obj_wrapper
def gong():
    print('self is gong')

# 多装饰器
def decorator_a(func):
    print('Get in decorator_a')

    def inner_a(*args, **kwargs):
        print('Get in inner_a')
        print("inner_a is to run %s" % func.__name__)
        return func(*args, **kwargs)

    return inner_a


def decorator_b(func):
    print('Get in decorator_b')

    def inner_b(*args, **kwargs):
        print('Get in inner_b')
        print("inner_b is to run %s" % func.__name__)
        return func(*args, **kwargs)

    return inner_b


def decorator_c(func):
    print('Get in decorator_c')

    def inner_c(*args, **kwargs):
        print('Get in inner_c')
        print("inner_c is to run %s" % func.__name__)
        return func(*args, **kwargs)

    return inner_c


@decorator_c
@decorator_b
@decorator_a
def to_double(x):
    """
        装饰顺序按靠近函数顺序执行（decorator_a->decorator_b->decorator_c），调用时由外而内(inner_c->inner_b->inner_a->to_double)，
        执行顺序和装饰顺序相反。
        装饰器也相当于是函数调用,就算不调用to_double(2)，decorator_a->decorator_b->decorator_c也会执行。
        因此上面inner函数和装饰器函数之间的代码会执行，即使不调用被装饰的to_double(x)函数
    :param x:
    :return:
    """
    print('Get in to_double')
    return x * 2


# bar()
# foo()
# square(5, 6)
# bar("bar")
# gong()
# to_double(2)
