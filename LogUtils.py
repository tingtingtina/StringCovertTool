#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import io  
import sys 

class Log:
    'Log util'

    # Log info
    @staticmethod
    def info(msg):
        print msg.encode("GBK", "ignore")

    # Log error
    @staticmethod
    def error(msg):
        # print('\033[31mError1')
        msg = msg.encode("GBK", "ignore")
        print(msg)

    # Log debug
    @staticmethod
    def debug(msg):
        print msg.encode("GBK", "ignore")
