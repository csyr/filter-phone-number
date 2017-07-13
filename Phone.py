#!/usr/bin/python
# -*- coding: UTF8 -*-

import urllib2, socket, re;
from PhoneRule import PhoneRule
from SMTPMail import SMTPMail
from UrlRequest import UrlRequest


class Phone:
    __URL = 'http://num.10010.com/NumApp/NumberCenter/qryNum?provinceCode=%s&cityCode=%s&monthFeeLimit=0&groupKey=&searchCategory=3&net=01&amounts=210&codeTypeCode=&searchValue=&qryType=01&goodsNet=4&_=%s'
    __num_prefix = [185, 186, 131, 156, 130, 155, 132, 176]
    __city_code = {'sh': (31, 310), 'bj': (11, 110), 'sz':(34,450)}
    default_city = 'sh'

    same_digit = 4
    display_digit = 3
    display_same_digit = 4

    def __init__(self, default_city=''):
        if default_city in ['bj', 'sh']:
            self.default_city = default_city

    def get_data(self, city='sh'):
        phone_list_all = []
        for prefix in self.__num_prefix:
            city_info = self.__city_code[city]
            url = self.__URL % (city_info[0], city_info[1], prefix)
            request = UrlRequest(url)
            self.phone_data = request.get_request()

            regex = ur"1[3-8]\d{9}"
            phone_list = re.findall(regex, self.phone_data)
            if phone_list and len(phone_list):
                phone_list_all.append(phone_list)
            self.phone_list = phone_list_all

    def send_mail(self, msg):
        mail = SMTPMail('pz_mail@126.com', '123455')
        mail.from_mail = 'pz_mail@126.com'
        mail.to_mail = 'pengzhan@mesway.com'
        mail.subject = 'Phone list'
        mail.message = msg
        mail.send()

    def run(self):
        self.get_data(self.default_city)
        phone_rule = PhoneRule(self.phone_list)
        same_digit_phone = phone_rule.same_digit(self.same_digit)
        display_digit_phone = phone_rule.display_digit(self.display_digit)
        display_same_digit_phone = phone_rule.display_same_digit(self.display_same_digit)
        if len(display_same_digit_phone) or (len(same_digit_phone) and len(display_digit_phone)):
            msg = "same digit: "+repr(same_digit_phone)
            msg += "<br /> display digit: " + repr(display_digit_phone)
            self.send_mail(msg)
            print msg


if __name__ == "__main__":
    phone = Phone()
    phone.run()
    phone.default_city = 'sh'
    phone.run()


