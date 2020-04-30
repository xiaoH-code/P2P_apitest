import json
import unittest
import requests

from utils import EncryptUtil


class TestMobile(unittest.TestCase):

    def test01_index(self):
        """获取首页信息"""
        url = "http://mobile-p2p-test.itheima.net/phone/index/index"

        # 请求参数
        req_data = {}

        # 对请求参数进行加密，并获取签名
        diyou = EncryptUtil.get_diyou(req_data)
        xmdy = EncryptUtil.get_xmdy(diyou)

        # 发送请求
        r = requests.post(url, data={"diyou": diyou, "xmdy": xmdy})
        print("r.text==", r.text)

        # 对响应数据进行解密
        json_data = r.json()
        diyou_data = json_data.get("diyou")
        decrypted_data = EncryptUtil.decrypt_data(diyou_data)
        print("decrypted_data=", decrypted_data)

        # 断言
        json_data = json.loads(decrypted_data)
        self.assertEqual(200, json_data.get("code"))
        self.assertEqual("success", json_data.get("result"))

    def test02_login(self):
        """登录"""
        url = "http://mobile-p2p-test.itheima.net/phone/member/login"

        # 请求参数
        req_data = {
            "member_name": "13012345678",
            "password": "test123"
        }

        # 对请求参数进行加密，并获取签名
        diyou = EncryptUtil.get_diyou(req_data)
        xmdy = EncryptUtil.get_xmdy(diyou)

        # 发送请求
        r = requests.post(url, data={"diyou": diyou, "xmdy": xmdy})
        print("r.text==", r.text)

        # 对响应数据进行解密
        json_data = r.json()
        diyou_data = json_data.get("diyou")
        decrypted_data = EncryptUtil.decrypt_data(diyou_data)
        print("decrypted_data=", decrypted_data)

        # 断言
        json_data = json.loads(decrypted_data)
        self.assertEqual(200, json_data.get("code"))
        self.assertEqual("success", json_data.get("result"))
