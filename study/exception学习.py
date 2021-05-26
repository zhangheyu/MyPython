import traceback


def test_raise(num):
    if int(num) < 10:
        raise Exception('太小了！！！！{}'.format(num), '第二个')


if __name__ == '__main__':
    num = input('请输入：')
    try:
        test_raise(num)
    except Exception as e:
        print(e.args)
        print(type(e))
        # print(e.message)


    try:
        print(x)
    except Exception as e:
        print(e)  # name 'x' is not defined
        print(str(e))  # name 'x' is not defined
        print(repr(e))  # NameError("name 'x' is not defined")
        # traceback.print_exc()

    try:
        100 / int(num)
    except ZeroDivisionError as e:
        print(e)   # division by zero

