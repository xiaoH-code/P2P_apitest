import logging
import unittest,requests
import random
import time

from parameterized import parameterized

from api.login_api import loginAPI
from utils import assert_util, DBUtls, read_verify_data


class test_login(unittest.TestCase):
    phone = '13088881111'
    reg_fail_phone = '13088881113'
    imVerifyCode = '8888'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    @classmethod
    def setUpClass(cls) -> None:
    #def tearDownClass(cls) -> None:
        sql1 = "delete from mb_member_register_log where phone in ('13088881111','13088881112','13088881113','13088881114');"
        DBUtls.delete(DBUtls.DB_MEMBER,sql1)
        print("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13088881111','13088881112','13088881113','13088881114');"
        DBUtls.delete(DBUtls.DB_MEMBER, sql2)
        print("delete sql = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13088881111','13088881112','13088881113','13088881114');"
        DBUtls.delete(DBUtls.DB_MEMBER, sql3)
        print("delete sql = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('13088881111','13088881112','13088881113','13088881114');"
        DBUtls.delete(DBUtls.DB_MEMBER, sql4)
        print("delete sql = {}".format(sql4))

    def test01_pic_verify_random(self):
        """测试图片验证码请求的随机字符为小数"""
        #构建测试数据
        r = random.random()
        #发送请求
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        #断言
        self.assertEqual(200,response.status_code)

    def test02_pic_verify_randint(self):
        """测试图片验证码请求的随机字符为整数"""
        #构建测试数据
        r = random.randint(1,1000000)
        #发送请求
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        #断言
        self.assertEqual(200,response.status_code)

    def test03_pic_verify_randchar(self):
        """测试图片验证码请求的随机字符为字母"""
        #构建测试数据
        r = ''.join(random.sample('abcdefghijklmn', 5))
        logging.info("r:{}".format(r))
        #发送请求
        response = self.login_api.get_pic_verify_code(self.session,r)
        #断言
        self.assertEqual(200,response.status_code)

    def test04_sms_verify_success(self):
        """测试获取短信验证码成功"""
        # 构建测试数据
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        self.assertEqual(200, response.status_code)
        #请求短信验证码
        logging.info('phone = {}'.format(self.phone))
        logging.info('imVerifyCode = {}'.format(self.imVerifyCode))
        response = self.login_api.get_sms_verify_code(self.session,self.phone,self.imVerifyCode,'reg')
        logging.info("response={}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"短信发送成功")
        # self.assertEqual(200,response.status_code)
        # self.assertEqual(200,response.json().get("status"))
        # self.assertIn("短信发送成功",response.json.get("description"))

    def test05_sms_verify_wrong_pic_code(self):
        """测试图片验证码错误时，获取短信验证码失败"""
        # 构建测试数据
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        #请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, self.phone, '1111', 'reg')
        logging.info("response={}".format(response.json()))
        #断言
        assert_util(self, response, 200, 100, "图片验证码错误")

    def test06_sms_verify_no_pic_verify(self):
        """测试不调用图片验证码接口时，请求短信验证码失败"""
        # 构建测试数据
        #请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session,self.phone,self.imVerifyCode,'reg')
        logging.info("response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"图片验证码错误")

    def test07_reg_success(self):
        """注册成功"""
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        self.assertEqual(200, response.status_code)
        #请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session,self.phone,self.imVerifyCode,'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self,response,200,200,"短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session,self.phone,'test123')
        logging.info("reg response={}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"注册成功")

    def test08_reg_phone_is_exist(self):
        """注册 - 手机号已存在"""
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session,str(r))
        self.assertEqual(200, response.status_code)
        #请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session,self.phone,self.imVerifyCode,'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self,response,200,200,"短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session,self.phone,'test123')
        logging.info("reg response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"手机已存在")

    def test09_reg_pwd_is_empty(self):
        """注册 - 密码为空"""
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, '13088881112', self.imVerifyCode, 'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session, '13088881112', '')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_util(self, response, 200, 100, "密码不能为空")

    def test10_reg_pic_verify_code_error(self):
        """注册 - 图片验证码错误"""
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, self.reg_fail_phone, self.imVerifyCode, 'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session, self.reg_fail_phone, 'test123','1234')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_util(self, response, 200, 100, "验证码错误")

    def test11_reg_sms_verify_code_error(self):
        """注册 - 短信验证码错误"""
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, self.reg_fail_phone, self.imVerifyCode, 'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session, self.reg_fail_phone, 'test123',phonecode='123456')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_util(self, response, 200, 100, "验证码错误")

    def test12_reg_no_promission(self):
        """不同意协议"""
        r = random.random()
        response = self.login_api.get_pic_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, self.reg_fail_phone, self.imVerifyCode, 'reg')
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.reg(self.session, self.reg_fail_phone, 'test123',dyserver='off')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_util(self, response, 200, 100, "验证码错误")

    def test13_login_success(self):
        """登录成功"""
        #发送登录请求
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"登录成功")

    def test14_username_is_not_exist(self):
        """用户名不存在"""
        #发送登录请求
        response = self.login_api.login(self.session,kw='13099212314')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"用户不存在")

    def test15_password_is_empty(self):
        """密码不能为空"""
        #发送登录请求
        response = self.login_api.login(self.session,pwd='')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_util(self,response,200,100,"密码不能为空")

    def test16_login_password_wrong(self):
        """多次密码错误时提示"""
        #第一次输入错误密码
        response = self.login_api.login(self.session,pwd='error')
        logging.info("密码错误1次，响应为：{}".format(response.json()))
        assert_util(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        # 第二次输入错误密码
        response = self.login_api.login(self.session, pwd='error')
        logging.info("密码错误2次，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        # 第三次输入错误密码
        response = self.login_api.login(self.session, pwd='error')
        logging.info("密码错误3次，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #登录-输入3次错误后再输入正确密码
        response = self.login_api.login(self.session)
        logging.info("密码错误3次后输入正确密码登录，响应为：{}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #登录60s发送登录请求，登录成功
        time.sleep(60)
        #发送登录请求
        response = self.login_api.login(self.session)
        logging.info("密码错误3次后等待60秒，输入正确密码登录，响应为：{}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")

    def test17_is_login_nologin(self):
        """未登录时判定是否登录"""
        #发送判断请求
        response = self.login_api.islogin(self.session)
        logging.info("islogin response={}".format(response.json()))
        #断言
        assert_util(self,response,200,250,"您未登陆！")

    def test18_is_login(self):
        """登录时判定是否登录"""
        #发送登录请求
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #判断是否登录
        response = self.login_api.islogin(self.session)
        logging.info("islogin response={}".format(response.json()))
        assert_util(self,response,200,200,"OK")