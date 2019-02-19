#!/usr/local/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor
 @file: main.py
 @time: 2018/11/5 15:59
"""

import time
from adb import By
from adb import Adb
import file
import random
import re

class Main:
    def __init__(self, port=None, device=None):

        # 用于查找失败三次时 程序暂停半小时
        self._flag = 0

        self._success = []
        self._failed = []
        self._dict = {'success': self._success, 'failed': self._failed}


        self._file = file.File()
        self._done_list=self._file.get_done_list()
        self._json = self._file.json()
        self._adb = Adb(password=self._json['password'],port=port, device=device)
        # config.json 配置信息
        # 查找联系人模式 file | loop
        self._mode = self._json['mode']
        # 循环首尾 包含首 不包含尾
        self._loop = self._json['loop']
        # 文件路径 手机号码一行一个
        self._input = self._json['file']
        # 自动切换账号 微信登录 微信预留账号
        self._account = self._json['account']
        # 累计查找结果达到指定个数 会从内存写入到文件
        self._dump = self._json['dump']
        # 切换账号达到一定次数 会休眠 单位分钟
        self._sleep = self._json['sleep-time']
        # 切换账号指定次数
        self._sleep_flag = self._json['sleep-flag']
        self._switch_when=self._json['switch-when']
        self._added_number=0

    # 输出添加结果到内存 或 文件
    def push(self, key: str, value):

        _list = self._dict[key]
        _list.append(value)

        # list到一定长度 输出到文件
        if int(self._dump) == len(_list):
            self._file.dump(_list, key)

    def init(self):
        self._adb.click_by_text_after_refresh('通讯录')
        self._adb.click_by_text_after_refresh('新的朋友')
        self._adb.click_by_text_after_refresh('添加朋友')
        self._adb.click_by_text_after_refresh('微信号/QQ号/手机号')

    def switch(self):
        self._adb.changeip()
        for i in range(6):
            self._adb.adb_put_back()
        self._adb.click_by_text_after_refresh('微信')
        time.sleep(2)
        self._adb.click_by_text_after_refresh('我')
        self._adb.click_by_text_after_refresh('设置')
        self._adb.click_by_text_after_refresh('切换帐号')
        self._adb.refresh_nodes()
        self._adb.find_nodes_by_text(self._account[0])
        left = float(self._adb.get_bounds()[0])

        self._adb.find_nodes_by_text(self._account[1])
        right = float(self._adb.get_bounds()[0])

        self._adb.find_nodes_by_text('当前使用')
        cursor = float(self._adb.get_bounds()[0])

        self._adb.find_nodes('true', By.naf)
        # 左侧用户在使用中
        if abs(cursor - left) < abs(cursor - right):
            self._adb.click(1)
        else:
            self._adb.click(0)
        # 判断是否登录成功
        while True:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('通讯录'):
                break
            time.sleep(2)
        self.init()
        self._flag += 1
        self._added_number = 0

    def switch_wcount(self):
        if int(self._sleep_flag) == self._flag:
            self.rest()
            self.switch()
        else:
            self.switch()


    def rest(self):
        print(' ---- 休眠中 ----')
        time.sleep(int(self._sleep) * 60)
        self._adb.unlock()
        self._flag = 0


    def add_friends(self, phone: str):
        print('===== 开始查找 ===== ' + phone + ' =====')
        self._adb.click_by_text_after_refresh('微信号/QQ号/手机号')

        # 输入号码
        self._adb.adb_input(phone)
        time.sleep(random.randint(1,3))
        # 点击搜索
        self._adb.click_by_text_after_refresh('搜索:' + phone)
        time.sleep(3+random.randint(1,3))
        print('  ==> 点击搜索 ==>  ')

        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('查找失败'):
            print('  <== 查找失败 <==  ')
            self.push('failed', phone + '\t查找失败')
            self._adb.adb_put_back()
            self.switch_wcount()

        elif self._adb.find_nodes_by_text('添加到通讯录'):
            self._adb.click(0)
            time.sleep(3+random.randint(1,3))
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('发送'):
                self._adb.click(0)
                time.sleep(6+random.randint(1,3))
            if self._adb.find_nodes_by_text('添加到通讯录') or self._adb.find_nodes_by_text('发消息'):
                print('  <== 发送成功 <==  ')
                self.push('success', phone)
                self._adb.adb_put_back()
            else:
                print('  <== 发送失败 <==  ')
                self.push('failed', phone + '\t发送失败')
                self._adb.adb_put_back()
                self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('发消息'):
            print('  <== 已经是好友 无需再次添加 <==  ')
            self.push('failed', phone + '\t已经是好友')
            self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('同时拥有微信和企业微信'):
            print('  <== 同时拥有微信和企业微信 <==  ')
            self.push('failed', phone + '\t同时拥有微信和企业微信')
            self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('该用户不存在') or self._adb.find_nodes_by_text('被搜帐号状态异常，无法显示'):
            print('  <== 该用户不存在 或 帐号异常 <==  ')
            self.push('failed', phone + '\t该用户不存在 或 帐号异常')
            self._adb.adb_put_back()
        elif self._adb.find_nodes_by_text('操作过于频繁，请稍后再试'):
            print('  <== 操作过于频繁 <==  ')
            self.push('failed', phone + '\t操作过于频繁')
            self._adb.adb_put_back()
            self.switch_wcount()
        else:
            print('  <== 未知原因 <==  ')
            self.push('failed', phone + '\t未知原因')
            self._adb.adb_put_back()
        self._added_number += 1
        # 清空已输入的字符
        self._adb.refresh_nodes()
        if self._adb.find_nodes('true', By.naf):
            self._adb.click(0)

    def main(self):
        self.init()
        print("The flowing number had been processed:")
        print(self._done_list)
        try:
            if 'file' == self._mode:
                with self._file.open(self._input) as f:
                    for line in f:
                        line = re.sub('\t.*','',line).strip()
                        if line not in self._done_list:
                            if self._switch_when == self._added_number:
                                self.switch_wcount()
                                self.add_friends(line)
                            else:
                                self.add_friends(line)
            elif 'loop' == self._mode:
                for line in range(int(self._loop[0]), int(self._loop[1])):
                    if str(line).strip() not in self._done_list:
                        self.add_friends(str(line))
        # 输出最后的添加结果
        finally:
            self._file.dump(self._success, 'success')
            self._file.dump(self._failed, 'failed')
            self._file.close()
