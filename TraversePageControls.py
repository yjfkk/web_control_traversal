import json
import os
import time
import urllib
from selenium import webdriver
from manager.Login import Login


class TraversePageControls(object):
    def __init__(self, config):
        # 类变量设置
        self.home_page = config['home_page']
        self.config = config
        self.inspected_path = ['/']
        self.host_name = ''
        self.to_inspect_urls = []
        # 初始化浏览器
        chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        # 登录
        Login(self.driver, self.config).do_login()

    def __del__(self):
        self.driver.close()

    def get_to_inspect_urls(self):
        self.driver.get(self.home_page)
        time.sleep(5)
        all_urls = self.driver.find_elements_by_tag_name('a')
        for one_url in all_urls:
            try:
                self.to_inspect_urls.append(one_url.get_property('href'))
            except Exception as e:
                print('url解析出错:' + e.args)

    def inspect(self, str_url):

        self.inspect_link(str_url)

    def inspect_link(self, str_url):
        try:
            url_parse = urllib.parse.urlparse(str_url)
            print(url_parse)
            self.host_name = url_parse.hostname
            self.driver.get(str_url)
            urls = self.driver.find_elements_by_tag_name('a')
            i = 0
            for i in range(len(urls)):
                url = urls[i]
                try:
                    url_str = url.get_property('href')
                    if self.url_verify(url_str):
                        url_parse = urllib.parse.urlparse(url_str)
                        self.inspected_path.append(url_parse.path)
                        if not url.is_enabled():
                            continue
                        url.click()
                        self.page_rule_matching(self.driver)
                        self.get_browser_log(self.driver)
                        hands = self.driver.window_handles
                        if len(hands) > 1:
                            self.driver.switch_to.window(hands[-1])
                            self.driver.close()
                            self.driver.switch_to.window(hands[0])
                            self.get_browser_log(self.driver)
                        if self.driver.current_url != str_url:
                            self.driver.get(str_url)
                except Exception as e:
                    print('遍历控件发生错误:' + str(e.args))
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except Exception as e:
                        print('错误发生适尝试寻找对话框失败：' + str(e.args))

                    continue
                urls = self.driver.find_elements_by_tag_name('a')
        except Exception as e:
            print('url解析出错：' + str(e.args))

    def main(self):
        self.get_to_inspect_urls()
        self.inspect(self.home_page)
        for one_url in self.to_inspect_urls:
            self.inspect(one_url)

    def url_verify(self, url_str):
        str_url = url_str
        url_parse = urllib.parse.urlparse(str_url)
        if self.host_name == url_parse.hostname and url_parse.path not in self.inspected_path:
            return True
        else:
            return False

    def get_browser_log(self, driver):
        logs = driver.get_log('browser')
        for log in logs:
            if log['level'] == 'WARNING':
                print(log)
                width = driver.execute_script("return document.documentElement.scrollWidth")
                height = driver.execute_script("return document.documentElement.scrollHeight")
                driver.set_window_size(width, height)
                driver.save_screenshot(os.path.join(os.getcwd(),'report','img',str(time.time())+'.png'))

    def page_rule_matching(self, driver):
        try:
            page_title = driver.title
            page_content = driver.page_source

            must_not_contain_title = self.config['page_rules']['must_not_contain']['title']
            must_not_contain_content = self.config['page_rules']['must_not_contain']['content']

            must_contain_title = self.config['page_rules']['must_contain']['title']
            must_contain_content = self.config['page_rules']['must_contain']['content']

            if page_title.find(must_not_contain_title) != -1 or page_content.find(must_not_contain_content) != -1:
                print('页面规则校验出错1')
            if page_title.find(must_contain_title) == -1 or page_content.find(must_contain_content) == -1:
                print('页面规则校验出错2')
        except Exception as e:
            print('页面规则校验出错：'+str(e.args))

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config.json'), 'rb') as f:
        config = f.read()
        config = json.loads(config)
    tpc = TraversePageControls(config)
    tpc.main()
    print(tpc.inspected_path)
