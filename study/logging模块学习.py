import logging
import os

'''
DEBUG： 详细信息，通常仅在诊断问题时才受到关注。整数level=10
INFO： 确认程序按预期工作。整数level=20
WARNING：出现了异常，但是不影响正常工作.整数level=30
ERROR：由于某些原因，程序 不能执行某些功能。整数level=40
CRITICAL：严重的错误，导致程序不能运行。整数level=50
默认的级别是WARNING,也就意味着只有级别大于等于的才会被看到，跟踪日志的方式可以是写入到文件中，也可以直接输出到控制台。
'''

# 输出到控制台
# logging.warning('Watch out!')  # 将输出到控制台
# logging.info('I told you so')  # 不会输出
# logging.error("an error occurrence！")  # 将输出到控制台

# 输出到文件中
module_name = str(os.path.basename(__file__)).split('.')[0]
log_name = module_name + '.log'
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename=log_name,
                    filemode='w',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志; a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error(f"{module_name} 模块日志")
