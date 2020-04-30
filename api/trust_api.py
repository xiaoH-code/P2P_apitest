import app

class trustAPI():
    def __init__(self):
        self.trust_register_url = app.BASE_URL + "/trust/trust/register"
        self.recharge_verify_url = app.BASE_URL + "/common/public/verifycode/"
        self.trust_recharge_url = app.BASE_URL + "/trust/trust/recharge"

    def trust_register(self,session):
        response = session.post(self.trust_register_url)
        return response

    def get_charge_verify_code(self,session,r):
        url = self.recharge_verify_url + r
        response = session.get(url)
        return response

    def trust_recharge(self,session,amount='1000',valicode='8888'):
        data = {"paymentType": "chinapnrTrust",
                 "formStr": "reForm",
                 "amount": amount,
                 "valicode": valicode}
        response = session.post(self.trust_recharge_url,data=data)
        return response