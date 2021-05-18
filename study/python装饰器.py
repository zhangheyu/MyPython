import logging


# 普通装饰器
def use_logging(func):
    def wrapper():
        logging.warning("%s is running" % func.__name__)
        # print("use_logging")
        return func()

    return wrapper


# 函数带参数的装饰器
def use_logging_with_param(func):
    def wrapper(*args, **kwargs):
        # args是一个数组，kwargs一个字典
        logging.warning("%s is running" % func.__name__)
        # print("use_logging_with_param")
        return func(*args, **kwargs)

    return wrapper


# 带参数的装饰器
def use_logging_dynamic_level(level):
    def decorator(func):
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


# bar()
# foo()
# square(5, 6)
# bar("bar")

gong()
