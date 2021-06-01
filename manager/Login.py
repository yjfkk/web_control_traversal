import json
import os


class Login(object):
    def __init__(self, driver,config):
        self.driver = driver
        self.config = config

    def do_login(self):
        try:
            self.driver.get(self.config['login']['login_page'])
            user_name_input =self.driver.find_element_by_css_selector(self.config['login']['login_user_input'])
            user_name_input.send_keys(self.config['login']['username'])

            password_input = self.driver.find_element_by_css_selector(self.config['login']['login_password_input'])
            password_input.send_keys(self.config['login']['password'])
            submit = self.driver.find_element_by_css_selector(self.config['login']['submit'])
            submit.click()
        except Exception as e:
            print('登录失败，请debug进行调试:'+str(e.args))
