# -*- coding: UTF8 -*-
import urllib2, socket;

class UrlRequest:

    def __init__(self, url=''):
        self.url = url

    # 使用Request
    def get_request(self, url=''):
        if not url:
            url = self.url
        if not url:
            return None
        # 可以设置超时
        socket.setdefaulttimeout(5)
        # 可以加入参数  [无参数，使用get，以下这种方式，使用post]
        # params = {"wd": "a", "b": "2"}
        # 可以加入请求头信息，以便识别
        i_headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
            "Accept": "text/plain"}
        # use post,have some params post to server,if not support ,will throw exception
        # req = urllib2.Request(url, data=urllib.urlencode(params), headers=i_headers)
        req = urllib2.Request(url, headers=i_headers)

        # 创建request后，还可以进行其他添加,若是key重复，后者生效
        # request.add_header('Accept','application/json')
        # 可以指定提交方式
        # request.get_method = lambda: 'PUT'
        try:
            page = urllib2.urlopen(req)
            response_data = page.read()
            if len(response_data) > 0:
                return response_data
                # like get
                # url_params = urllib.urlencode({"a":"1", "b":"2"})
                # final_url = url + "?" + url_params
                # print final_url
                # data = urllib2.urlopen(final_url).read()
                # print "Method:get ", len(data)
        except urllib2.HTTPError, e:
            print "Error Code:", e.code
        except urllib2.URLError, e:
            print "Error Reason:", e.reason