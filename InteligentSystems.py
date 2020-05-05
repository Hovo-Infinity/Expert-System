#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:48:08 2020

@author: hovhannesstepanyan
"""

from Fuzzy import FS_plot_cat, FS_intersect
import numpy as np

class InteligentSystems:
    
    def FS_func(FSx, Uy, Func = lambda x, Ux, Uy: np.array([1]*len(Uy)), method='minimax'):
        masx = FSx.items()
        Ux = np.array(list(masx)).T[0]
        masmu = np.array([0] * len(Uy))
        if method == 'minimax':
            for el in Ux:
                masmu=np.max([masmu, np.min([Func(el, Ux, Uy), [FSx[el]] * len(Uy)], axis=0)], axis=0)
        elif method == 'probability':
            for el in Ux:
                mn = Func(el, masx, Uy) * FSx[el]
                masmu = masmu + mn - masmu * mn
        else:
            print("Unknown method", method)
        return dict(np.array([Uy, masmu]).T)
    
    def FS_f(x, Ux, Uy):
        minx = np.min(Ux)
        miny = np.min(Uy)
        maxy = np.max(Uy)
        k = float(x - minx) / float(Ux.max() - minx)
        gran = k * (maxy - miny) + miny
        return np.array([1. if y == gran else 
                         float(y - miny) / (gran - miny) if y < gran else 
                         float(maxy - y) / (maxy - gran) for y in Uy])
    
    def FClass(Ux, Func = lambda x, Ux: np.array([1]*len(Ux)), method='base'):
        massiv = np.array([Func(el, Ux) for el in Ux])
        if method == 'base':
            masmu = np.min(massiv / np.max([list(zip(el, massiv.T[nom]))
                                           for nom, el in enumerate(massiv)],
                                          axis = 2), axis = 1)
        elif method == 'alternative':
            masmu = np.min(massiv / massiv.T, axis = 1)
        else:
            masmu = np.array([0] * len(Ux))
            print('Unknown method', method)
        return dict(np.array([Ux, masmu]).T)
    
    def FSU(x, Fg):
        Fgt = Fg.T
        ress = 0.
        if x <= np.min(Fgt[0]):
            ress = Fg[np.argmin(Fgt[0])][2]
        elif x >= np.max(Fgt[1]):
            ress = Fg[np.argmax(Fgt[1])][3]
        else:
            kt = Fg[(Fgt[0] <= x) & (Fgt[1] >= x)][0]
            ress = (x - kt[0]) / (kt[1] - kt[0]) * (kt[3] - kt[2]) + kt[2]
        return ress
    
    def free_FS(U, Fg, Func=FSU):
        return dict([[el, Func(el, Fg)] for el in U])
    
    def free_FS_cat(X, Fg, Func=FSU):
        return dict([[nom, Func(el, Fg)] for nom, el in enumerate(X)])
    
    def dis_help_sys(datas):
        names = datas[0]
        names.pop()
        names.pop(0)
        Ca_cat = names
        arrayToPlot = []
        criterias = []
        for i in range(1, len(datas)):
            row = datas[i]
            T = row.pop()
            criteria = row.pop(0)
            FCS = InteligentSystems.make_FG(min(row), max(row), T)
            criterias.append(criteria)
            FS_cat = InteligentSystems.free_FS_cat(list(map(float, row)), FCS)
            arrayToPlot.append(FS_cat)
        
        FR1c = FS_intersect(arrayToPlot)
        FR2c = FS_intersect(arrayToPlot, method='probability')
        FS_plot_cat([FR1c, FR2c], U=Ca_cat,
                    labels=['minimax', 'probability'], title='Արդյունք',
                   colors=['red', 'green', 'blue', 'yellow', 'green', 'purple'],
                   name='result')


    def make_FG(x1, x2, T):
        if T == 'U':
            return np.array([[int(x1) - 10, int(x2) + 10, 0., 1.]])
        elif T == 'N':
            return np.array([[int(x1) - 10, int(x2) + 10, 1., 0.]])
        else:
            return np.array([[0., 1., 0., 1.]])