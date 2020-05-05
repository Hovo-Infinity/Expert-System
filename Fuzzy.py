#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:36:03 2020

@author: hovhannesstepanyan
"""

from matplotlib import pylab as plt
from matplotlib import colors
import numpy as np
from itertools import product
import os


path = os.path.expanduser("~/Documents/")

def triangle_FS(U, a=None, b=None, c=None, d=None, h=1, form='equal'):
    if form in ['equal', 'greater', 'less']:
        if a is None:
            a = U.min()
        if c is None:
            c = U.max()
        if b is None:
            if d is None:
                b = (a + c) / 2
            else:
                b = d
        if d is None:
            d = b
        Mu = dict()
        if a > U.min():
            for el in U[U <= a]:
                Mu[el] = h if form == 'less' else 0.
        if c < U.max():
            for el in U[U >= c]:
                r = h if form == 'greater' else 0.
                z = Mu.get(el, 0)
                Mu[el] = r if r > z else z
        if a < b:
            for el in U[(U >= a) * (U <= b)]:
                r = 0. if form == 'greater' else h * float(el - a) / (b - a) if form == 'equal' else h * float(
                    b - el) / (b - a)
                z = Mu.get(el, 0)
                Mu[el] = r if r > z else z
        if b < d:
            for el in U[(U >= b) * (U <= d)]:
                r = h if form == 'equal' else 0.
                z = Mu.get(el, 0)
                Mu[el] = r if r > z else z
        if d < c:
            for el in U[(U >= d) * (U <= c)]:
                r = 0. if form == 'less' else h * float(el - d) / (c - d) if form == 'greater' else h * float(
                    c - el) / (c - d)
                z = Mu.get(el, 0)
                Mu[el] = r if r > z else z
        return Mu
    else:
        print("Unknown form")
        return None


def FS_plot(FS, _colors=None, labels=None, title=None, name=None, show=False):
    if _colors is None:
        _colors = list(reversed(list(colors.cnames.keys())))
    for idx, el in enumerate(FS):
        mas = np.array(sorted(el.items(), key=lambda x: x[0])).T
        if labels is None:
            lab = ' '
        else:
            lab = labels[idx]
        plt.plot(mas[0], mas[1], color=_colors[idx], label=lab)
    if not (labels is None):
        plt.legend(loc='upper right')
    if not (title is None):
        plt.title(title)
    if not (name is None):
        plt.savefig(path + name + '.png', format='png', dpi=100)
    if show:
        plt.show()
        
def F_And(FV, method='minimax'):
    if method == 'minimax':
        return np.min(FV)
    elif method == 'probability':
        return np.product(FV)
    elif method == 'adjective':
        if len(FV) == 2:
            return np.max([0, np.sum(FV) - 1])
        else:
            return np.max([0, np.sum([FV[-1], F_And(FV[:-1], method=method)]) - 1])
    else:
        print("Unknown method", method)
        return None


def F_Or(FV, method='minimax'):
    if method == 'minimax':
        return np.max(FV)
    elif method == 'probability':
        mu = 0
        for el in FV:
            mu = mu + el - mu * el
        return mu
    elif method == 'adjective':
        if len(FV) == 2:
            return np.min([1, np.sum(FV)])
        else:
            return np.min([1, np.sum([FV[-1], F_And(FV[:-1], method=method)])])
    else:
        print("Unknown method", method)
        return None


def F_Not(F):
    return 1 - F
    
def aplha_srez(FS, alpha=0.5):
    _alpha = 1e-10 if alpha == 0 else alpha
    mas = np.array(list(FS.items())).T
    return set(mas[0][mas[1] >= _alpha])


def FS_moment(FS, center=None):
    mas = np.array(list(FS.items())).T
    if center is None:
        Cgr = FS_Cgr(FS)
    else:
        Cgr = center
    return np.sum(mas[1] * np.square(mas[0] - Cgr))


def FS_Cgr(FS):
    mas = np.array(list(FS.items())).T
    return sum(mas[0] * mas[1]) / sum(mas[1])

def FS_quantificator(FS, quantificators=[u'more']):
    mas = np.array(list(FS.items())).T
    for el in np.flip(quantificators, axis=0):
        if el == u'more':
            mas[1] = np.square(mas[1])
        elif el == u'maybe':
            mas[1] = np.sqrt(mas[1])
        elif el == u'not':
            mas[1] = 1 - mas[1]
        else:
            print("unknown quantificator", el)
    return dict(mas.T)

def FS_union(FSs, PS=None, method='minimax'):
    U = set()
    for FS in FSs:
        U = set.union(U, FS.keys())
    res=dict()
    for el in U:
        s_mu = []
        for idx, FS in enumerate(FSs):
            p = 1 if PS is None else PS[idx]
            s_mu.append(F_And([p, FS.get(el, 0)], method=method))
        res[el] = F_Or(s_mu, method=method)
    return res

def FS_intersect(FSs, PS=None, method='minimax'):
    U = set()
    for FS in FSs:
        U = set.union(U, FS.keys())
    res=dict()
    for el in U:
        s_mu = []
        for idx, FS in enumerate(FSs):
            p = 1 if PS is None else PS[idx]
            s_mu.append(F_And([p, FS.get(el, 0)], method=method))
        res[el] = F_And(s_mu, method=method)
    return res


def FS_diff(FS1, FS2):
    U = set.union(set(), FS1.keys(), FS2.keys())
    res = dict()
    for el in U:
        mu1 = FS1.get(el, 0)
        mu2 = FS2.get(el, 0)
        res[el] = 0 if mu2 > mu1 else mu1 - mu2
    return res

def FS_compare(FS1, FS2, method='COG', IIR_F=lambda x: 1 if x > 0 else 0, IIR_method='minimax'):
    if method=='COG':
        COG1 = FS_Cgr(FS1)
        COG2 = FS_Cgr(FS2)
        return COG1 > COG2
    elif method == 'IIR':
        res = []
        for p1, p2 in list(product(FS1.keys(), FS2.keys())):
            res.append(F_And([FS1[p1], FS2[p2], IIR_F(p1 - p2)], method=IIR_method))
        return F_Or(res, method=IIR_method)
    else:
        print("Unknown method")
        return None
    
def FS_arifm_operation_Num(FS, num, operation=lambda x, y: x + y):
    mas1 = np.array(list(FS.items())).T
    mas1[0] = operation(mas1[0], num)
    return dict(mas1.T)
    
def FS_arifm_operation_Set(FS1, FS2, operation = lambda x, y: x + y, method = 'minimax', clearing = False):
    res = dict()
    for p1, p2 in list(product(FS1.keys(), FS2.keys())):
        res[operation(p1, p2)] = F_Or([F_And([FS1[p1], FS2[p2]], method=method), res.get(operation(p1, p2), 0)],
                                     method=method)
    if clearing:
        res1 = dict()
        res2 = dict()
        mas_T = sorted(res.items(), reverse = True, key = lambda x: x[0])
        mu = -1
        for el in mas_T:
            if el[1] >= mu:
                res1[el[0]] = el[1]
                mu = el[1]
        mas_T = sorted(res.items(), reverse = False, key = lambda x: x[0])
        mu = -1
        for el in mas_T:
            if el[1] >= mu:
                res2[el[0]] = el[1]
                mu = el[1]
        return FS_union([res1, res2])
    else:
        return res
            

def FS_plot_cat(FS, U=None, colors=list(reversed(list(colors.cnames.keys()))), labels = None, title=None, name=None, show=False):
    kols = len(FS)
    h1 = 0.9 / kols
    h2 = 1. / kols
    plt.ylim([0, 1])
    rr = np.array(range(len(FS[0])))
    for idx, el in enumerate(FS):
        mas = np.array(sorted(el.items(), key = lambda x: x[0])).T
        if (labels is None):
            lab = ' '
        else:
            lab = labels[idx]
        plt.bar(rr - 0.5 + h2 / 2. + h1 * idx, mas[1], width = h1, label = lab, color = colors[idx])
    if not(U is None):
        plt.xticks(rr, U)
    else:
        plt.xticks(rr)
    if not(labels is None):
        plt.legend(loc='upper right')
    if not(title is None):
        plt.title(title)
    if not(name is None):
        plt.savefig(path + name + '.png', forma='png', dpi=100)
    if show:
        plt.show()