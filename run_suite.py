import unittest,app,time
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.test_login_param import test_login_param
from script.test_login import test_login
from script.test_approve import test_approve
from script.test_tender_process import test_tender_process
from script.test_trust import test_trust
from script.test_tender import test_tender

#生成测试套件
suite = unittest.TestSuite()

#添加测试用例集合到测试套件中
suite.addTest(unittest.makeSuite(test_login))
suite.addTest(unittest.makeSuite(test_login_param))
suite.addTest(unittest.makeSuite(test_approve))
suite.addTest(unittest.makeSuite(test_trust))
suite.addTest(unittest.makeSuite(test_tender))
suite.addTest(unittest.makeSuite(test_tender_process))
#定义生成测试报告的路径
#report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d %H%M%S"))
report_file = app.BASE_DIR + "/report/report.html"
#使用HTMLTestRunner来生成测试报告
with open(report_file,'wb') as f:
    runner = HTMLTestRunner(f,title='P2P项目测试报告')
    runner.run(suite)