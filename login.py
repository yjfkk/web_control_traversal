import json
import os


class Login(object):
    def __init__(self, driver):
        with open(os.path.join(os.getcwd(), 'config.json')) as f:
            config = f.read()
            self.config = json.loads(config)
            self.driver = driver

    def do_login(self):
        try:
            self.driver.get(self.config['login_page'])
            user_name_input =self.driver.find_element_by_css_selector(self.config['login_user_input'])
            user_name_input.send_keys(self.config['username'])

            password_input = self.driver.find_element_by_css_selector(self.config['login_password_input'])
            password_input.send_keys(self.config['password'])
            submit = self.driver.find_element_by_css_selector(self.config['submit'])
            submit.click()
        except Exception as e:
            print('登录失败，请debug进行调试:'+str(e.args))
