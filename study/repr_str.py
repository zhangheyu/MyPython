import logging

content = "张翮誉".encode('utf-8')
str = '{!s}'.format('\xe4\xb8\xad\xe6\x96\x87\xe5\x88\x86\xe7\xbb\x84')
print('repr:{!r}'.format(content))
print('str:{!s}'.format(content))
print(content)
print(str)

logging.error(content)