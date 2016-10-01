#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'huybery'

import json


def get_reg():
    """
    输入正则表达式
    """
    # reg = raw_input("Please input your regular expression : ")
    reg = '(a|b)*abb'
    return reg


def set_nfa():
    """
    设置 NFA 的数据结构
    """
    nfa = {}
    nfa["k"] = []
    nfa["e"] = []
    nfa["f"] = {}
    nfa["s"] = [0]
    nfa["z"] = []
    return nfa


def reg_to_nfa(reg, nfa):
    """
    遍历正则表达式，构造nfa
    """
    count = 0
    i = 0
    parentheses = []
    words = []
    stack = []
    for i in range(0, len(reg)):
        token = reg[i]
        if token == '(':
            for s in range(i, len(reg)):
                parentheses.append(reg[s])
                if reg[s] == ')':
                    break
            print ''.join(parentheses)
        if token == '*':
            pass
        else:
            # 给 NFA 增加转换字母
            words.append(token)
            # 给 NFA 增加一个状态
            nfa["k"].append(count)
            count = count + 1

    nfa["e"] = list(set(words))
    # print nfa
    return nfa

if __name__ == '__main__':
    reg = get_reg()
    nfa = set_nfa()
    reg_to_nfa(reg, nfa)
