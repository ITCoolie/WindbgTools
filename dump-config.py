#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
# 该脚本用于windbg分析时依据版本号配置symbol、image、src路径，以及打印dump栈回溯
# author: yujian221 # gmail.com
# 
import os, sys
#################################################
## windbg调试分析脚本
#################################################
import pykd
import argparse
import getpass
import re

############################ 配置部分 ###########################
## symbol路径
SYS_SYMBOL = 'symbols'
sympath = ""
## exe路径
exepath = ""
## 源码路径
srcpath = ''
ATLPATH = 'C:/Program Files (x86)/Microsoft Visual Studio 8/VC/atlmfc/include;'
############################ 配置部分结束 #######################

## 显示帧变量
def listFrameDetails():
    print 'Listing frame details...'
    FRAME_NUM = 30
    out = ''
    for j in range(0, FRAME_NUM):
        out = pykd.dbgCommand('.frame ' + str(j))
        if out is None:
            return
        pykd.dprintln(out)
        out = pykd.dbgCommand('dv /i/t/V')
        if out is None:
            return
        pykd.dprintln(out)

## 依据版本号读取配置
def readConfig(version):
    global sympath   ## symbo路径
    global exepath   ## image路径
    global srcpath   ## 源代码路径

    print 'Get the system enviroment...'
    python_home = os.environ.get('PYTHON_HOME')
    product_env = os.environ.get('PRODUCT_ENV')
    print 'PYTHON_HOME=', python_home, ' PRODUCT_ENV=', product_env
    win_symbol = '%s/%s' %(product_env, SYS_SYMBOL)

    ## 生成windbg symbol、image、src路径
    sympath = '%s/%s/pdb;%s;cache*%s;srv*https://msdl.microsoft.com/download/symbols' %(product_env, version, win_symbol, win_symbol)
    exepath = '%s/%s/image/' %(product_env, version)
    srcpath = '%s/%s/src/;%s' %(product_env, version, ATLPATH)

##  配置windbg
def set_env(_sympath, _exepath, _srcpath):
    print 'Setting windbg enviroment...'
    print pykd.dbgCommand('.sympath ' + _sympath)
    print pykd.dbgCommand('.exepath ' + _exepath)
    print pykd.dbgCommand('.srcpath ' + _srcpath)

##  分析dump
def analyze():
    print 'Analyzing dump...'
    s = pykd.dbgCommand('.reload')
    s = pykd.dbgCommand('!analyze -v')
    pykd.dprintln(s)

    ## 打印dump分析的栈回溯
    for i in s.split("\n"):
        if ("STACK_COMMAND" in i):
            index = i.index(':')
            cmd = i[index+1:]
            print cmd  
            s = pykd.dbgCommand(cmd)
            pykd.dprintln(s)
            s = pykd.dbgCommand('kn 20')
            pykd.dprintln(s)
            listFrameDetails()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is windbg analyze script!')
    parser.add_argument('--v', action="store", dest="version", default=getpass.getuser())
    given_args = parser.parse_args()
    version = given_args.version;
    readConfig(version)
    set_env(sympath, exepath, srcpath)
    analyze()
