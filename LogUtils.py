#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import io  
import sys 

class Log:
    'Log util'

    # Log info blue
    @staticmethod
    def info(msg):
        print('\033[34m')
        print msg

    # Log error red
    @staticmethod
    def error(msg):
        print('\033[31m')
        print msg.encode("GBK", "ignore")

    # Log debug white
    @staticmethod
    def debug(msg):
        print('\033[37m' + msg.encode("GBK", "ignore"))
