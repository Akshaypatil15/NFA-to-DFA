#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'huybery'
import json
from collections import deque


def get_data(input):
    """
    读取NFA源文件
    """
    nfa = json.load(open(input, 'r'))
    return (set(nfa["k"]), set(nfa["e"]), nfa["f"], set(nfa["s"]), set(nfa["z"]))


def set_cache(e_set):
    """
    设置缓存，来记录每一个进行过闭包的状态
    """
    cache = {}
    for i in e_set:
        cache[i] = {}
    cache['#'] = {}
    return cache


def move(f, cache, I, arc):
    """
    弧转换接口
    """
    return closure(f, cache[arc], I, arc)


def ep_closure(f, cache, I):
    """
    ε闭包
    """
    return closure(f, cache["#"], I, '#')


def closure(f, cache, I, arc):
    """
    闭包的实现
    """
    res = set()
    for i in I:
        if not i in cache:
            cache[i] = set()
            # 判断转换弧为ε时
            if arc == '#':
                cache[i] = set([i])
            # 实现 move
            if i in f:
                if arc in f[i]:
                    # 如果为ε进行递归继续向前转换
                    if arc == '#':
                        cache[i] |= closure(f, cache, set(f[i][arc]), arc)
                    else:
                        cache[i] = set(f[i][arc])
        # 得到闭包后的缓存
        res |= cache[i]
    return res


def set_dfa(e_set):
    """
    设置dfa的数据结构,其中字母表保持不变
    """
    dfa = {}
    dfa["k"] = []
    dfa["e"] = list(e_set)
    dfa["f"] = {}
    dfa["s"] = []
    dfa["z"] = []
    return dfa


def calc_dfa(k_set, e_set, f, s_set, z_set):
    """
    实现转换流程
    """
    # 初始化 DFA 结果数据结构，字母表不变
    dfa = set_dfa(e_set)
    # 构造 DFA 结果队列
    dfa_set = []
    # 初始化缓存，将字母表作为键
    cache = set_cache(e_set)
    # 对初始态 ε-closure(I)
    ep = ep_closure(f, cache, s_set)
    # 初始化双向列表，实现高效插入删除（任务队列）
    queue = deque([ep])
    # 结果队列内放入 NFA 经过ε闭包后的初态
    dfa_set.append([ep])
    dfa["k"].append("0")
    dfa["s"].append("0")
    # 若ep状态存在终态集 设为 DFA 终态集
    if not len(ep & z_set) == 0:
        dfa["z"].append("0")
    i = 0
    # 任务队列循环
    while queue:
        # 取出需要进行转移的状态
        T = queue.popleft()
        j = ""
        index = str(i)
        i = i + 1
        dfa["f"][index] = {}
        # 进行弧转换后进行ε闭包
        for s in e_set:
            # 下一状态
            t = ep_closure(f, cache, move(f, cache, T, s))
            try:
                # 这次状态是否存在于结果队列
                j = str(dfa_set.index(t))
            except ValueError:
                queue.append(t)
                j = str(len(dfa_set))
                dfa_set.append(t)
                dfa["k"].append(j)
            dfa["f"][index][s] = j
            if not len(t & s_set) == 0:
                dfa["s"].append(j)
            if not len(t & z_set) == 0:
                dfa["z"].append(j)

    return dfa


def output_dfa(dfa, f):
    """
    输出DFA
    """
    f = open(f, "w")
    dfa_json = json.dumps(dfa, indent=4, sort_keys=False, ensure_ascii=False)
    f.write(dfa_json)
    f.close()
    # print dfa_json


def main():
    """
    主函数
    """
    (k_set, e_set, f, s_set, z_set) = get_data("NFA.json")
    dfa = calc_dfa(k_set, e_set, f, s_set, z_set)
    output_dfa(dfa, "DFA.json")


if __name__ == '__main__':
    """
    测试样例是书 p58 图 4.4 转换成功。
    """
    main()
