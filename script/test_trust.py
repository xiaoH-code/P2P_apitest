import logging
import random

import requests,unittest
from api.login_api import loginAPI
from api.trust_api import trustAPI
from utils import assert_util, request_third_api


class test_trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()
        #登录成功
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")

    def tearDown(self) -> None:
        self.session.close()

    def test01_trust_register(self):
        """开户"""
        #获取开户信息
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response={}".format(response.json()))
        #断言获取的开户信息是否正确
        self.assertEqual(200,response.status_code)
        self.assertEqual(200, response.json().get("status"))
        #获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        #发送第三方的请求，请求第三方接口进行开户
        response = request_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        #断言第三方接口请求处理是否成功
        self.assertEqual('UserRegister OK',response.text)

    def test02_recharge(self):
        """充值"""
        #获取充值验证码
        r = random.random()
        response = self.trust_api.get_charge_verify_code(self.session,str(r))
        self.assertEqual(200,response.status_code)
        logging.info("get_recharge_code response={}".format(response.text))

        #充值
        amount = '1000'
        response = self.trust_api.trust_recharge(self.session,amount)
        logging.info("recharge response={}".format(response.text))
        #断言获取的开户信息是否正确
        self.assertEqual(200,response.status_code)
        self.assertEqual(200, response.json().get("status"))
        #获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        #发送第三方的请求，请求第三方接口进行开户
        response = request_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        #断言第三方接口请求处理是否成功
        self.assertEqual('NetSave OK',response.text)

