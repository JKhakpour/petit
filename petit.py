#encoding: utf-8
from __future__ import unicode_literals
import re
from itertools import groupby
from operator import mul, add
from functools import reduce
import math
import constants
# 2 <=> 3 stuff:
try:
    from itertools import izip as zip
except ImportError:
    pass
try:
  basestring
except NameError: # code is running on python 3.x?
  basestring = str

__version__ = '0.1.1'

def text_to_num(s):
    class NumberException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)

    def get_simple_number(text):
        text = text.strip()
        if text in constants.Ignore:
            return ''
        elif constants.Small.get(text, None):
            return constants.Small.get(text)
        elif constants.Magnitude.get(text, None):
            return constants.Magnitude.get(text)
        else:
            raise NumberException("Unknown number: "+w)

    def is_Magnitude(n):
        if n == 10:
            return False
        i = 100
        while (i <= n):
            if i == n:
                return True
            i *= 10
        return False

    s = s.strip()
    if s.startswith(constants.NEG.strip()):
        sign = -1
        s = s.replace(constants.NEG.strip(), '', 1).strip()
    else:
        sign = 1
    a = [m.strip() for m in re.split(r"( | \u0648 )+", s)]
    a = [get_simple_number(m) for m in a if m and m not in constants.Ignore]
    groups = groupby(zip([None] + a, a), key=lambda x: x[1] in constants.Magnitude.values() and (not(x[0]) or (x[0] < x[1])))

    a = []
    for is_magnitude, g in groups:
        g = (x[1] for x in g)
        if is_magnitude:
            a.append(reduce(mul, g, 1))
        else:
            a.append(reduce(add, g, 0))
    ## now a is sequence of Simple, Magnitude, Simple, Magnitude, ...  
    n = 0
    g = 0
    if len(a) == 0:
        raise NumberException('No number recognized!')
    if len(a) == 1:
        n = a[0]
    else:
        seq = zip(a, a[1:]+[None])
        x , y = next(seq)
        try:
            while True:
                if y and (g + x) < y and is_Magnitude(y):
                    g += x
                    g *= y
                    x, y = next(seq) # skip one bi-gram
                    x, y = next(seq)
                else:
                    if g:
                        n += g
                        g = 0
                    else:
                        n += x
                        x, y = next(seq)
        except StopIteration:
            pass

    return sign*n

def num_to_text(number = 0):
    def three_digit(number):
        result = ''
        if (number < 10):
            result += constants.DIGITS_WORD[number]
        elif (number < 20):
            result += constants.TEENS[number - 10]
        elif (number < 100):
            result += (constants.TENS[int(number / 10)] + constants.AND +  three_digit(number % 10)) if(number % 10) else constants.TENS[int(number / 10)]
        elif (number < 1000):
            result += constants.HUNDREDS[int(number / 100)] + constants.AND + three_digit(number % 100) if(number % 100) else constants.HUNDREDS[int(number / 100)]
        return result.replace('  ', ' ').strip()

    if isinstance(number, basestring) and number.isdigit():
        number = int(number)
    #number is int? to int
    if number < 0:
        result = constants.NEG + num_to_text(abs(number))
    elif number == 0:
        result = three_digit(number)
    elif len(str(number)) > 3*len(constants.POWERS_OF_THOUSAND):
        raise ValueError("number is toooo big!")
    else:
        td = [(((number//(10**i))%10**3),i) for i in  range(0, len(str(number)), 3)]
        td = [(digit, order) for digit, order in td if digit][::-1]
        result = constants.AND.join([(three_digit(digit) + constants.POWERS_OF_THOUSAND[int(order/3)]) for digit, order in td])
    return result.replace('  ', ' ').strip()

def num_to_ordinal(number = 0):
    #number is int? convert to int
    if isinstance(number, basestring) and number.isdigit():
        number_s = number
        number = int(number)
    else:
        number_s = str(number)
    result = ''
    if (number_s in constants.IRREG_ORD_NUMS):
        result = constants.IRREG_ORD_NUMS[number_s]
    elif (any(m.match(number_s) for m in constants.IRREG_ORD_REGEXES)):
        match = list(filter(lambda m: m if m.match(number_s) else None, constants.IRREG_ORD_REGEXES))[-1]
        repls = constants.IRREG_ORD_REGEXES[match]
        result = constants.AND.join([num_to_text(match.sub(repl, number_s)) for repl in repls[:-1]] + [num_to_ordinal(match.sub(repls[-1], number_s))])
    else:
        result = num_to_text(number).rstrip() + constants.MIM.lstrip()
    return result.replace('  ', ' ').strip()

