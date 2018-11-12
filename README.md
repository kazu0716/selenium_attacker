Selenium Attacker 
====

## Overview

Password list attack to mezzanine admin page for internal test by using selenium

## Requirement
- python3
- pip3
- git
- Web Browser
  - this Poc-code use Chrome, if you would like to use other browser, you should change code in main.py
- Browser Driver
  - this Poc-code use chromedriver for MacOS, and so you should replace for your envirment when you don't use Mac

## Usage

- basic usage
```
(selenium_attacker) kazu0716 MacBook-Pro-4 $ python attacker.py
2018/02/22 02:33:02 - User: admin, Pass: admin, Result: Succeeded
2018/02/22 02:33:03 - ------------------------------------------------
2018/02/22 02:33:03 - Senario-3 : ログイン -> 特定4URLにアクセス
2018/02/22 02:33:03 - Access lists: ユーザー->内容->ページ

2018/02/22 02:33:03 - Logout: True
2018/02/22 02:33:03 - ----------------
2018/02/22 02:33:03 - Run senario
2018/02/22 02:33:03 - Clicked: ユーザー
2018/02/22 02:33:04 - Clicked: 内容
2018/02/22 02:33:07 - Clicked: ページ
2018/02/22 02:33:08 - Logout
```

- modify user_id and password 

```
(selenium_attacker) kazu0716 MacBook-Pro-4 $ head -n 3 account_list.csv
admin,admin@example.com,admin
richard59,richard59@green.biz,@2~OMZ025
melindajones,melindajones@lane.com,k9N?OPj76*fO
```

- attcker config file

```
[general]
url=http://127.0.0.1:8000/ja/admin/login/
account=username
#account=email
driver=phantomjs
#driver=chrome
ip_type=random

[interval]
max=1
min=1

[senario]
pattern=0

# pattern 設定値説明
# 1 ログイン -> 特定1URLにアクセス -> ログアウトする
# 2 ログイン -> 特定1URLにアクセス -> ログアウトしない
# 3 ログイン -> 特定4URLにアクセス -> ログアウトする
# 4 ログイン -> 特定4URLにアクセス -> ログアウトしない
# 5 ログイン -> ランダムな1URLにアクセス -> ログアウトする
# 6 ログイン -> ランダムな1URLにアクセス -> ログアウトしない
# 7 ログイン -> ランダムな4URLにアクセス -> ログアウトする
# 8 ログイン -> ランダムな4URLにアクセス -> ログアウトしない
# 9 ログイン -> ランダムな1～5URLにアクセス -> ログアウトする
# 0 ログイン -> ランダムな1～5URLにアクセス -> ログアウトしない
# 上記以外 ログインのみ
```

## Install

```
git clone https://github.com/kazu0716/selenium_attacker.git
cd selenium_attacker/
pip3 install -r requirement.txt
python3 attacker.py
```
