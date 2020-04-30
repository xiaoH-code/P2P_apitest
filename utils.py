import json
import logging
import unittest

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




