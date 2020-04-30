import app

class loginAPI():
    def __init__(self):
        self.get_pic_verify_code_url = app.BASE_URL + '/common/public/verifycode1/'
        self.get_sms_verify_code_url = app.BASE_URL + '/member/public/sendSms'
        self.reg_url = app.BASE_URL + '/member/public/reg'
        self.login_url = app.BASE_URL + '/member/public/login'
        self.islogin_url = app.BASE_URL + '/member/public/islogin'

    def get_pic_verify_code(self,session,r):
        url = self.get_pic_verify_code_url + r
        response = session.get(url)
        return response

    def get_sms_verify_code(self,session,phone,imgVerifyCode,type):
        data = {"phone": phone,
                "imgVerifyCode": imgVerifyCode,
                "type": type}
        response = session.post(self.get_sms_verify_code_url,data=data)
        return response

    def reg(self,session,phone,pwd,verifycode='8888',phonecode='666666',dyserver='on'):
        data = {"phone": phone,
                 "password": pwd,
                 "verifycode": verifycode,
                 "phone_code": phonecode,
                 "dy_server": dyserver}
        response = session.post(self.reg_url,data=data)
        return response

    def login(self,session,kw='13012345678',pwd='test123'):
        data = {"keywords": kw,"password": pwd}
        response = session.post(self.login_url,data=data)
        return response

    def islogin(self,session):
        response = session.post(self.islogin_url)
        return response