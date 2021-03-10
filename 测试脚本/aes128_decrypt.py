# AES-demo

import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''


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
    text = 'KC4865'
    # 包含中文会报错，暂时不知道原因
    # text = '浙KC4865'
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    print(f'加密后: {encrypted_text}')


# 解密方法
def decrypt_oralce():
    # 秘钥
    key = '123456789'
    # 密文
    text = 'GuTOaQdv/efySg7t2IsrBQ=='
    # text = 'ZGzL21KRDjZMbK4qStkMXg=='     川H6C48U
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='gb2312'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='gb2312').replace('\0', '')
    print(f'解密后: {decrypted_text}')


if __name__ == '__main__':
    encrypt_oracle()
    decrypt_oralce()
