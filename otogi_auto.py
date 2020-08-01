import os
import random
import time
from enum import Enum
import gc

import numpy as np
import win32con
import win32gui
from cv2 import cv2
from PIL import ImageGrab, ImageOps, Image
from pykeyboard import PyKeyboard
from pymouse import PyMouse


class Status(Enum):
    start = 0
    connecting = 1
    finish = 2
    ok = 3
    fuhuo = 4
    giveup = 5
    go = 6
    master999 = 7
    nofriends = 8
    repeact = 9
    result = 10
    back = 11
    hundred = 12


class Otogi_Auto(object):

    hwnd_title = dict()
    chrome_handle = 0
    scale = 1.25
    m = PyMouse()
    k = PyKeyboard()
    total_count = 0

    def __init__(self):
        self.connecting_pic = cv2.imread(
            os.path.join("sysFile", "Image", "connecting.png"))
        self.finish_pic = cv2.imread(
            os.path.join("sysFile", "Image", "finish.png"))
        self.ok_pic = cv2.imread(os.path.join("sysFile", "Image", "ok.png"))
        self.fuhuo_pic = cv2.imread(
            os.path.join("sysFile", "Image", "fuhuo.png"))
        self.giveup_pic = cv2.imread(
            os.path.join("sysFile", "Image", "giveup.png"))
        self.go_pic = cv2.imread(os.path.join("sysFile", "Image", "go.png"))
        self.master999_pic = cv2.imread(
            os.path.join("sysFile", "Image", "master999.png"))
        self.nofriends_pic = cv2.imread(
            os.path.join("sysFile", "Image", "nofriends.png"))
        self.repeat_pic = cv2.imread(
            os.path.join("sysFile", "Image", "repeat.png"))
        self.result_pic = cv2.imread(
            os.path.join("sysFile", "Image", "result.png"))
        self.back_pic = cv2.imread(
            os.path.join("sysFile", "Image", "back.png"))
        self.hundred_pic = cv2.imread(
            os.path.join("sysFile", "Image", "100.png"))

        self.th_connecting, self.tw_connecting = self.connecting_pic.shape[:2]
        self.th_finish, self.tw_finish = self.finish_pic.shape[:2]
        self.th_ok, self.tw_ok = self.ok_pic.shape[:2]
        self.th_fuhuo, self.tw_fuhuo = self.fuhuo_pic.shape[:2]
        self.th_giveup, self.tw_giveup = self.giveup_pic.shape[:2]
        self.th_go, self.tw_go = self.go_pic.shape[:2]
        self.th_master999, self.tw_master999 = self.master999_pic.shape[:2]
        self.th_nofriends, self.tw_nofriends = self.nofriends_pic.shape[:2]
        self.th_repeat, self.tw_repeat = self.repeat_pic.shape[:2]
        self.th_result, self.tw_result = self.result_pic.shape[:2]
        self.th_back, self.tw_back = self.back_pic.shape[:2]
        self.th_hundred, self.tw_hundred = self.hundred_pic.shape[:2]
        self.status = Status.start
        self.search_chrome()
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(
            self.chrome_handle)
        print('top:', self.top)
        print('left:', self.left)
        print('bottom:', self.bottom)
        print('right:', self.right)
        win32gui.ShowWindow(self.chrome_handle, win32con.SW_SHOW)
        self.do_repeact_func()

    def search_chrome(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        for h, t in self.hwnd_title.items():
            if t is not "":
                if 'Google Chrome' in t:
                    # print('谷歌')
                    print(hex(h), t)
                    self.chrome_handle = h
                    print(self.chrome_handle)

    def get_all_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    def do_repeact_func(self):
        image = ImageGrab.grab().convert('L')
        image1 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(
            image1, self.repeat_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        if max_val > 0.85:
            print("重复按钮存在")
            self.status = Status.repeact
            self.m.click(self.left+10+int(tl[0]/self.scale)+random.randint(
                1, 50), self.top+5+int(tl[1]/self.scale)+random.randint(1, 10))
            while(self.status == Status.repeact):
                self.do_ok_after_battle_func()
                time.sleep(3)
        else:
            print('不存在')

    def do_ok_after_battle_func(self):
        image = ImageGrab.grab().convert('L')
        image1 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(
            image1, self.ok_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        if max_val > 0.85:
            print("ok按钮存在")
            self.status = Status.ok
            self.m.click(self.left+10+int(tl[0]/self.scale)+random.randint(
                1, 50), self.top+5+int(tl[1]/self.scale)+random.randint(1, 10))
            while(self.status == Status.ok):
                self.do_connecting_func()

    def do_connecting_func(self):
        battle_count = 0
        image = ImageGrab.grab().convert('L')
        # image.show()
        image1 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(
            image1, self.connecting_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        if max_val > 0.85:
            print("正在连接中")
            self.status = Status.connecting
            while(self.status == Status.connecting):
                battle_count += 1
                time.sleep(10)
                print("战斗计数: ", battle_count)
                self.do_result_func()

    def do_fuhuo_func(self):
        pass

    def do_result_func(self):
        image = ImageGrab.grab().convert('L')
        image1 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(
            image1, self.result_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        if max_val > 0.70:
            print("正在结算中")
            self.total_count += 1
            print("已完成战斗次数: ", self.total_count)
            self.status = Status.result
            while(self.status == Status.result):
                self.do_repeact_func()
                time.sleep(5)

    def do_start_statu_check(self):
        image = ImageGrab.grab().convert('L')
        image1 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(
            image1, self.result_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        if max_val > 0.70:
            self.status = Status.result
        result = cv2.matchTemplate(
            image1, self.hundred_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc


Otogi_Auto()
