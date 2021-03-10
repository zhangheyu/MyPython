# AES-demo

import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''

def pad(text):
    """
    #填充函数，使被加密数据的字节码长度是block_size的整数倍
    """
    length = AES.block_size
    count = len(text.encode('gb2312'))
    add = length - (count % length)
    entext = text + ('\0' * add)
    return entext

# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 加密方法
def encrypt_oracle():
    # 秘钥
    key = '123456789'
    # 待加密文本
    # text = '浙KC4865'
    text = '甘L8888W'
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(pad(text).encode("gb2312"))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='gb2312')  # 执行加密并转码返回bytes
    print(f'{text} 加密后: {encrypted_text}')


# 解密方法
def decrypt_oralce():
    # 秘钥
    key = '123456789'
    # 密文
    # text = 'GuTOaQdv/efySg7t2IsrBQ=='       # 浙KC4865
    # text = 'ZGzL21KRDjZMbK4qStkMXg=='       # 川H6C48U
    text = '/XqrbCh+NvRbtJnchyZc6A=='
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='gb2312'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='gb2312').replace('\0', '')
    print(f'{text} 解密后: {decrypted_text}')


if __name__ == '__main__':
    encrypt_oracle()
    decrypt_oralce()
