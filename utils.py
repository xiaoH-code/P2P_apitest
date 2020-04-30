import logging
import unittest
import base64
import hashlib
import json
import re
from Crypto.Cipher import AES

import pymysql
import requests
from bs4 import BeautifulSoup

import app


def assert_util(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertIn(desc, response.json().get("description"))

def request_third_api(form_data):
    # 解析响应数据
    soup = BeautifulSoup(form_data, 'html.parser')
    url = soup.form['action']
    data = {}
    for input in soup.find_all("input"):
        data.setdefault(input['name'], input['value'])
    logging.info("data = {}".format(data))
    response = requests.post(url, data=data)
    return response

class DBUtls:
    DB_MEMBER = "czbk_member"  # 会员数据库
    DB_FINANCE = "czbk_finance"  # 财务数据库

    @classmethod
    def get_conn(cls,db_name):
        conn = pymysql.connect(app.DB_URL, app.DB_USERNAME, app.DB_PASSWORD, db_name,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor=None,conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)


def read_verify_data(file_name,method_name,param_names):
    file = app.BASE_DIR + "/data/" + file_name
    test_data = []
    with open(file,encoding='utf-8') as f:
        verify_data = json.load(f)
        case_data_list = verify_data.get(method_name)
        for case_data in case_data_list:
            test_case_data = []
            for param in param_names.split(","):
                param_data = case_data.get(param)
                test_case_data.append(param_data)
            test_data.append(test_case_data)
    print('json data={}'.format(test_data))
    return test_data

# 加解密工具类
class EncryptUtil:
    # 发送请求时，加密密码
    SEND_AES_KEY = ";3jm$>/p-ED^cVz_j~.KV&V)k9jn,UAH"
    # 发送请求时，签名密钥
    SEND_SIGN_KEY = "DY34fdgsWET@#$%wg#@4fgd345sg"
    # 接收数据时，解密密钥
    RECEIVE_AES_KEY = "54Ms5bkE6UEdyrRviJ0![OR]g+i79x]k"

    @staticmethod
    def padding_pkcs5(value):
        BS = AES.block_size
        return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))

    # 替换空字符
    @staticmethod
    def replace_blank(str_data):
        str_data = re.compile("\t|\r|\n").sub("", str_data)
        print("replace_blank str_data=", str_data)
        return str_data

    @staticmethod
    def aes_encrypt(key, data):
        """
        AES加密
        :param key: 密钥
        :param data: 待加密数据
        :return: 加密后数据
        """
        data = base64.encodebytes(data.encode()).decode()
        # 替换特殊字符
        data = EncryptUtil.replace_blank(data)
        print("data=", data)

        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)

        # 解密
        padding_value = EncryptUtil.padding_pkcs5(data)
        encrypt_aes = aes.encrypt(padding_value)

        # 用base64转成字符串形式
        encrypted_text = base64.encodebytes(encrypt_aes).decode()
        return encrypted_text

    @staticmethod
    def aes_decrypt(key, data):
        """
        AES解密
        :param key: 密钥
        :param data: 待解密数据
        :return: 解密后数据
        """
        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(data.encode())

        # 执行解密
        decrypted_bytes = base64.decodebytes(aes.decrypt(base64_decrypted))
        # 转换为字符串
        decrypted_text = str(decrypted_bytes, encoding="utf-8")

        # 把Unicode转成中文
        result = decrypted_text.encode().decode("unicode_escape")
        return result

    @staticmethod
    def md5value(data):
        print("md5value data=", data)
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()

    @staticmethod
    def get_diyou(data):
        # 把字典转换为JSON字符串
        if isinstance(data, dict):
            data = json.dumps(data)
        aes_encrypt_data = EncryptUtil.aes_encrypt(EncryptUtil.SEND_AES_KEY, data)
        return EncryptUtil.replace_blank(aes_encrypt_data)

    @staticmethod
    def get_xmdy(data):
        return EncryptUtil.md5value(
            EncryptUtil.SEND_SIGN_KEY + EncryptUtil.replace_blank(data) + EncryptUtil.SEND_SIGN_KEY)

    @staticmethod
    def decrypt_data(data):
        return EncryptUtil.aes_decrypt(EncryptUtil.RECEIVE_AES_KEY, data)