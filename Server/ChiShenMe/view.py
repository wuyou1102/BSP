# -*- encoding:UTF-8 -*-
from django.shortcuts import render
from datetime import datetime
import os


def foods(request):
    context = dict()
    context['foods'] = __get_foods()
    context['period'] = __get_period()
    return render(request, 'ChiShenMe.html', context)


def __get_foods():
    lst = list()
    with open('Server/ChiShenMe/foods.txt') as f:
        for line in f.readlines():
            lst.append(line.strip('\r\n'))
    return " ".join(lst)


def __get_period():
    now = datetime.now().hour + 8
    if now in range(5, 10):
        return u"早饭"
    elif now in range(10, 16):
        return u"中饭"
    elif now in range(16, 21):
        return u"晚饭"
    elif now in range(21, 24) or now in range(0, 5):
        return u"夜宵"
    else:
        return u"今天"
