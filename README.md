# PyLex

A simple lex by python :snake:

Copyright (C) 2016 huybery All rights reserved.

# Intro

PyLex 是一个 `lex` 的 `python` 简单实现，包含了如下功能：

- [ ] 实现 `regular expression` -> `NFA`
- [x] 实现 `NFA` -> `DFA`
- [ ] `DFA` 最小化
- [ ] `miniDFA` -> 词法分析器

`RE` -- Thompson --> `NFA` -- 子集构造算法 --> `DFA` -- Hopcroft --> `词法分析器代码`

注：这个版本只用来学习参考，**请勿用于生产环境**

# Requirements

Environment： `python2.7`  
DataType： `json`  
System： `archlinux`

# How to Use

- `git clone git@github.com:huybery/NFA-to-DFA.git`
- fill the NFA data in `NFA.json`
- run  `python2 convert.py`
- cat `DFA.json`
- You will see a miracle :smile:

# Documentation

## 如何表示 NFA 和 DFA

大部分教材是用临接矩阵来表示数据的，我觉得不如直接使用五元组的键值对方便。

如典型的 `NFA` 可以表示为：

```json
{
  "k": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
  "e": ["a", "b"],
  "f": {
    "0": {
      "#": ["1", "7"]
    },
    "1": {
      "#": ["2", "4"]
    },
    "2": {
      "a": ["3"]
    },
    "3": {
      "#": ["6"]
    },
    "4": {
      "b": ["5"]
    },
    "5": {
      "#": ["6"]
    },
    "6": {
      "#": ["1", "7"]
    },
    "7": {
      "a": ["8"]
    },
    "8": {
      "b": ["9"]
    },
    "9": {
      "b": ["10"]
    }
  },
  "s": ["0"],
  "z": ["10"]
}
```

数据文档

| 变量        | 意义           |
| ------------- |:-------------:|
| k      | 状态集 |
| e      | 字母表 |
| f | 转换函数 |
| s | 初态  |
| z | 终态 |
| # | ε |

## 闭包的实现

原理是一个递归，通过判断转移时的条件来决定下一个状态

```python
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
```

## move 和 ε 闭包

其实这两个作用方式是基本相同的 所以可以整合到 `closure` 接口中

```python
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
```

## 引入缓存（cache）

因为在进行转移的时候其实做了大量的重复性转移  
所以自己构造了一个缓存机制来优化速度 性能得到大幅度提升

```python
def set_cache(e_set):
    """
    设置缓存，来记录每一个进行过闭包的状态
    """
    cache = {}
    for i in e_set:
        cache[i] = {}
    cache['#'] = {}
    return cache
```

## 转换流程的实现

代码里基本每一步都写了注释 可读性应该很好  
实现想法是构造两个队列 一个任务队列一个结果队列  


```python
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
```

# 心得

搞懂原理之后用手去演算真实费心费力，所以就决定用代码来实现  
最后用动态规划做了优化  大概花了一上午时间...  
写过之后对 `子集构造法` 有了更深刻的理解

# License

GPL-3.0

Copyright (c) 2016 Huybery
