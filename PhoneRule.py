# -*- coding: UTF8 -*-

import re

class PhoneRule:

    def __init__(self, phone_list =[]):
        if isinstance(phone_list, list):
            self.phone_list = phone_list
        else:
            self.phone_list = []

    #连续相同数字的号码 times：相同数字的位数 如：AAAA,BBB,CC
    def same_digit(self, times = 2):
        if times<2 or times>8:
            times = 2
        match_phone = []
        for display_times in range(times, 8):
            for i in range(10):
                regex = ur"["+repr(i)+"]{"+repr(display_times)+"}"
                reg_obj = re.compile(regex)
                for phone in self.phone_list:
                    if reg_obj.search(repr(phone)):
                        match_phone.append(phone)
        return match_phone

    def __get_unique_list(self, data_list):
        unique_list = []
        for item in data_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list;

    #后8位数中唯一出现的数字的总数 times:唯一数字的数量 如：ABCBACDA,ACBCABAC
    def display_digit(self, times = 3):
        if times<2 or times>8:
            times = 2
        match_phone = []
        for phone in self.phone_list:
            sub_phone = phone[3:]
            sub_phone_list = self.__get_unique_list(list(sub_phone))
            if len(sub_phone_list) <= times:
                match_phone.append(phone)
        return  match_phone

    def __count_display_times(self, target, str):
        target = repr(target)
        same_digit_list = re.findall(ur"["+repr(str)+"]", target)
        return  len(same_digit_list)

    #后8位里面【0-9】某个数字同时出现的大于等于次数（times）的手机号
    def display_same_digit(self, times = 5):
        if times > 8 or times < 2:
            times = 5
        match_phone = []
        for phone in self.phone_list:
            sub_phone = phone[3:]
            for i in range(9):
                if self.__count_display_times(sub_phone, i) >= times:
                    match_phone.append(phone)
        return  self.__get_unique_list(match_phone)