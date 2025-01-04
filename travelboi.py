#Last updated 1/7/2023
import math
import itertools
import numpy as np
import time

def setstartpoint(x):
    if type(x) == tuple and len(x) == 2:
        SP = x
    else:
        SP = None
    return SP

#There are four sets of points of interest (selected by z)
#Each point of interest is a positive x, y coordinate on one of four grids
def setspec(z):
    if z == 'AEg':
        WS = np.asarray([(25.1, 73.3),
                        (55, 81),
                        (56, 44.9),
                        (49.09, 77.54),
                        (60.92, 75.84)])
        AzS = np.asarray([(16.4, 38.5),
                          (67, 13.2),
                          (17.8, 21.7)])
        OP = np.asarray([(79.2, 83.8)])
        Th = np.asarray([ (55.2, 30.5),
                         (59.5, 38.4)])
    elif z == 'Jc':
        WS = np.asarray([(43.32, 66.60),
                        (50.4, 45.1),
                        (33.9, 63.7)])
        AzS = np.asarray([(45.0, 61.3),
                          (44.6, 61.2),
                          (46.23, 40.84)])
        OP = np.asarray([(25.2, 35.4),
                         (61.8, 13)])
        Th = np.asarray([(59.8, 65.2),
                         (56.91, 43.72),
                         (59.5, 38.4)])
    elif z == 'LT':
        WS = np.asarray([(39, 86),
                        (64.3, 25.4),
                        (74.7, 37.9),
                        (24.9, 69.7)])
        AzS = np.asarray([(12.5, 49.4),
                          (16.7, 38.8),
                          (57.5, 41.3),
                          (16.2, 38.8),
                          (40.7, 54.4)
                          ])
        OP = np.asarray([(82.45, 50.67),
                         (86.4, 53.7),
                         (35.34, 40.12),
                         (66.1, 52.9)
                         ])
        Th = np.asarray([(27.96, 45.79),
                         (56.8, 30.5),
                         (60.4, 79.7),
                         (58.6, 45.8)])
    elif z == 'IEh':
        WS = np.asarray([(57.5, 83.6),
                        (68.0, 26.8),
                        (57.5, 58.5),
                        (67.87, 57.96)
                        ])
        AzS = np.asarray([(46.23, 40.84),
                          (38.5, 59.2),
                          (45.1, 61.2),
                          (21, 45),
                          (46.2, 23.9),
                          (43.7, 30.9)
                          ])
        OP = np.asarray([(64.42, 18.7),
                         (61.4, 67.6),
                         (85.7, 25.2)
                         ])
        Th = np.asarray([(59.9, 70.4),
                         (13.2, 63.68),
                         (56.3, 41.2),
                         (47.24, 40.1),
                         (56.1, 40.9)])
    else:
        WS, AzS, OP, Th = []
    return WS, AzS, OP, Th

SP = setstartpoint((44.28, 68.54))
WS, AzS, OP, Th = setspec('Jc')

#Change local coordinates to standard coordinates across the entire search space
#The Th grid starts at 0,0. The other grids are offset from it by the translations below.
WSdif = np.asarray([[-28, -35]])
AzSdif = np.asarray([[-20, 77]]) 
OPdif = np.asarray([[-59, 25]]) 
Thdif = np.asarray([[0, 0]])
WS += WSdif
AzS += AzSdif
OP += OPdif
Th += Thdif
pts = np.vstack([WS, AzS, OP, Th])
print(pts)
print(pts.shape)

x = pts[:,0:1]
y = pts[:,1:2]
#xn = pts[:,0][:,None] #alternate form of forming 2d array with 1 column
#yn = pts[:,1][:,None]
dist = np.sqrt((x-x.T)**2+(y-y.T)**2) #array x-x.T is difference between each x value

idxpts = np.arange(len(pts))
routes = itertools.permutations(idxpts)
routes = list(routes)
costs = []
#This algorithm brute forces the permuations, which for the 'JC' route is ~40 million.
#If this was more than an experiment, I would research routing algorithms. I presume someone at Google Maps or a similar company has a more efficient solution.
#Even instantiating routes to calculate length can cause a memory crash above a ~14 permutations
#print(f'Number of permutations: {len(routes)}.')

for i, route, in enumerate(routes):
    if i%1000000 == 0 and i > 0:
        print(i, costs[np.argmin(costs)], costs[np.argmax(costs)], time.ctime())
    if SP == None:
        cost = 0.0
    else:
        cost = math.dist(SP, tuple(pts[route[0]]))#
    for n in range(len(route)-1):
        cost += dist[route[n],route[n+1]]
    if i < 500:
        costs.append(cost)
    if i >= 500:
        if cost < costs[np.argmax(costs)]:
            costs[np.argmax(costs)] = cost

imin = np.argmin(costs)
WS0, AzS0, OP0, Th0 = setspec('LT')
pts0 = np.vstack([WS0,AzS0, OP0, Th0])
tags = (len(WS), len(AzS), len(OP), len(Th))

print(f'Distance: {costs[imin]}.')
print(f'Best permutation: {imin}.', routes[imin])
for idx in routes[imin]:
    if idx < tags[0]:
        print(idx, "WS", pts0[idx])
    elif idx in range(tags[0], sum(tags[0:2])):
        print(idx, "AzS", pts0[idx])
    elif idx in range(sum(tags[0:2]), sum(tags[0:3])):
        print(idx, "OP", pts0[idx])
    else:
        print(idx, "Th", pts0[idx])
print(time.ctime())
