#!/usr/bin/python
# -*- coding: UTF8 -*-

import os,re

def check_process(path):
    path_list = path.split('/')
    app = path_list[-1]
    process_list = os.popen("ps aux|grep node").readlines()
    regex = repr(app)
    has_process = False
    for item in process_list:
        if re.match(regex, item):
            has_process = True

    if not has_process:
        os.popen("/usr/bin/node "+path)


if __name__ == '__main__':
    check_process('/data/webroot/touch.mescake.com/init.js')



