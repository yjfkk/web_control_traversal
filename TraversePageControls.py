import json
import os
import urllib
from selenium import webdriver
from login import Login


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
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(1)
        # 登录
        Login(self.driver, self.config).do_login()

    def __del__(self):
        self.driver.close()

    def get_to_inspect_urls(self):
        self.driver.get(self.home_page)
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
                        url.click()
                        hands = self.driver.window_handles
                        if len(hands) > 1:
                            self.driver.switch_to.window(hands[-1])
                            self.driver.title
                            self.get_browser_log(self.driver)
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


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config.json')) as f:
        config = f.read()
        config = json.loads(config)
    tpc = TraversePageControls(config)
    tpc.main()
    print(tpc.inspected_path)
