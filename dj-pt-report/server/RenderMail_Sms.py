__author__ = 'yunbinan'
# coding:utf-8
import os, sys


class BizCodeSendStrip:
    def __init__(self, bizCode, send, strip):
        self.bizCode = bizCode
        self.send = send
        self.strip = strip

    def __str__(self):
        return '%s\t%s\t%s' % (self.bizCode, self.send, self.strip)


if __name__ == '__main__':
    bizCodeSendStrip = BizCodeSendStrip('abc', 12, 24)
    print bizCodeSendStrip

