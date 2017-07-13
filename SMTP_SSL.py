
#-*- encoding: utf-8 -*-

import os, sys, string, socket
import smtplib

'''
method:
    smtp = SMTP_SSL('192.168.2.10')
    smtp.set_debuglevel(1)
    smtp.sendmail("zzz@xxx.com", "zhaowei@zhaowei.com", "xxxxxxxxxxxxxxxxx")
    smtp.quit()
'''

class SMTP_SSL (smtplib.SMTP):
    def __init__(self, host='', port=465, local_hostname=None, key=None, cert=None):
        self.cert = cert
        self.key = key
        smtplib.SMTP.__init__(self, host, port, local_hostname)
        
    def connect(self, host='localhost', port=465):
        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                host, port = host[:i], host[i+1:]
                try: port = int(port)
                except ValueError:
                    raise socket.error, "nonnumeric port"
        if not port: port = 654
        if self.debuglevel > 0: print>>stderr, 'connect:', (host, port)
        msg = "getaddrinfo returns an empty list"
        self.sock = None
        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                if self.debuglevel > 0: print>>stderr, 'connect:', (host, port)
                self.sock.connect(sa)
                # 新增加的创建ssl连接
                sslobj = socket.ssl(self.sock, self.key, self.cert)
            except socket.error, msg:
                if self.debuglevel > 0: 
                    print>>stderr, 'connect fail:', (host, port)
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg

        # 设置ssl
        self.sock = smtplib.SSLFakeSocket(self.sock, sslobj)
        self.file = smtplib.SSLFakeFile(sslobj);

        (code, msg) = self.getreply()
        if self.debuglevel > 0: print>>stderr, "connect:", msg
        return (code, msg)
