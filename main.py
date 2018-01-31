# -*- coding: utf-8 -*-

import os

from selenium import webdriver


def main():
    try:
        driver = webdriver.Chrome(os.path.normpath(os.path.join(os.path.abspath('__file__'), '../driver/chromedriver')))
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(10)
        driver.get("http://127.0.0.1:8000/ja/admin/")

    except Exception as e:
        print(e)

    finally:
        driver.close()


if __name__ == '__main__':
    main()
