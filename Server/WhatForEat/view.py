# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os


def foods(request):
    context = dict()
    context['foods'] = __get_foods()
    return render(request, 'WhatForEat.html', context)


def __get_foods():
    return []
