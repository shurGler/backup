# -*- coding: utf-8 -*-

# -- Sheet --

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# # resource
# https://github.com/fluentpython/example-code-2e


# # Chapter 1 — The Python Data Model
# 
# **Sections with code snippets in this chapter:**
# 
# * [A Pythonic Card Deck](#A-Pythonic-Card-Deck)
# * [Emulating Numeric Types](#Emulating-Numeric-Types)


# ## A Pythonic Card Deck


# #### Example 1-1. A deck as a sequence of playing cards


import collections

# https://docs.python.org/zh-cn/3/library/collections.html#collections.namedtuple
# 元组工厂函数，构建只有少数属性但是没有方法的对象，metaclass/元类
Card = collections.namedtuple('Card', ['rank', 'suit'])
type(Card)

# 构造牌堆类
class FrenchDeck: # py 3
# class FrenchDeck(object): # py 2
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

# 方块七
beer_card = Card('7', 'diamonds')
beer_card

deck = FrenchDeck()
len(deck)
# magic method, 特殊方法，dunder mehtod（double underline）->双下方法
len(deck) == deck.__len__() == FrenchDeck.__len__(deck)

deck[0]
# test 1
deck[0] == deck.__getitem__(0) == FrenchDeck.__getitem__(deck, 0)

deck[-1]

# NBVAL_IGNORE_OUTPUT
from random import choice

choice(deck)

# slicing
deck[:3]

# 从12号开始，步长13输出
deck[12::13]

# python 核心语言特性——迭代
for card in deck:
    print(card)

# python 标准库方法，由于内置了__getitem__
for card in reversed(deck):
    print(card)

# 迭代通常是隐式的，如果添加__contains__方法可能会更快，这里采用的是迭代搜索
Card('Q', 'hearts') in deck

Card('7', 'beasts') in deck

# 排序规则：2<……<A，黑桃<红桃<方块<梅花
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck, key=spades_high):
    print(card)

# ### 性能
# 调用内置len方法，会更快，由于 Cpython 会直接访问内存中长度可变的内置对象的C语言结构体（？？？）


# ## Emulating Numeric Types


# #### Example 1-2. A simple two-dimensional vector class


import math

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # 也可以实现 __str__ 方法，与 __repr__ 方法的区别在于，前者便于console用户查看值，后者便于debug用户查看变量值与类型
    def __repr__(self):
        # 勘误：前者的好处在于可以检查数据类型必须要为数值而不是字符串，否则报错
        # FACT：这里的repr函数也不会报错，由于 %r是一种字符串格式化的占位符，用于将一个值转换为其对应的字符串表示形式。
        return 'Vector(%r, %r)' % (self.x, self.y)
        # return f'Vector({self.x}, {self.y})'

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # return bool(abs(self))
        # better, evaluating short-circuits
        return bool(self.x or self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

# check
Vector(1, '2')
Vector(1, '2') + Vector(1, '2')
# abs(Vector(1, '2'))
bool(Vector(0, 1)), bool(Vector(1, 1)), bool(Vector(1, 0)), bool(Vector(0, 0))

v1 = Vector(2, 4)
v2 = Vector(2, 1)
v1 + v2

v = Vector(3, 4)
abs(v)

v * 3

abs(v * 3)

# why 数据模型而不是对象模型  
# https://docs.python.org/3/reference/datamodel.html
# 
# 用一套丰富的元对象协议对语言进行扩展，从而支持新的编程范式——面向方面编程。例如：zope.interface


