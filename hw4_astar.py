try:
    import time
except:
    ImportError
try:
    import numpy as np
except:
    ImportError
try:
    import sys, random
except:
    ImportError
try:
    from math import sqrt
except:
    ImportError
try:
    import os
except:
    ImportError
try:
    import csv
except:
    ImportError
try:
    from copy import deepcopy
except:
    ImportError
try:
    import sys
except:
    ImportError
try:
    import Queue as q
except:
    ImportError
try:
    from collections import deque
except:
    ImportError


start_time = time.time()

##Creates the distance matrix
def cartesian_matrix(coords):
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx, dy = x1-x2, y1-y2
            dist=sqrt(dx*dx + dy*dy)
            matrix[i,j] = dist
    return matrix

##Function to compute the G heuristic
def computeG(explored, current, cm):

    dis2 = 0
    dis1 = []
    j=1
    i = 0
    flag = 0
    while flag==0:
        if len(explored) >1:
            if j == (len(explored)+1):
                flag = 1
                break
            x1 = explored[i]
            if j == (len(explored)):
                x2 = current
                dis1 = cm[x1,x2]
                dis2 = dis2 + dis1
                j=j+1
                i = i+1
            else:
                x2 = explored[j]
                dis1 = cm[x1,x2]
                dis2 = dis2 + dis1
                j=j+1
                i = i+1
        else:
            x1 = explored[i]
            dis1 = cm[x1,x1]
            dis2 = dis2 + dis1
            flag = 1
    x2 = explored[-1]
    dis3 = cm[x2,current]
    dis2 = dis2 +dis3    
    return dis2

##Calculates the length of the tourxs
def tour_length(matrix, tour,CITIES):
    total = 0
    t = tour
    for i in range(CITIES):
        j      = (i+1)%CITIES
        total += matrix[t[i], t[j]]
    return total

##Calculates the distance from the current city to the nearest unvisited city
def partA(unexplored, explored, nodes, cm):
    dis = []
    indices = []
    current = deepcopy(nodes)

    for unex in unexplored:
        if current == unex:
            if len(unexplored)==1:
                current = 0
                dis.append(cm[current,unex])
                indices.append(unex)
            else:
                continue            
        else:
            dis.append(cm[current,unex])
            indices.append(unex)
    minDis = min(dis)
    indexMin = dis.index(minDis)
    index = indices[indexMin]
                
    return index, minDis

##MST calculates the estimated distance to travel all the unvisited cities 
def partB(unexplored, current,index,cm,explored):
    exp = []
    distance_temp = []
    unexp = deepcopy(unexplored)
    distance = []
    primTour = []
    x1 = 0
    x2 = 0
    xArr = []
    yArr = []
    i = 0
    j = i+1
    while(j<(len(unexp))):
        x1 = unexp[i]
        x2 = unexp[j]
        distance.append(cm[x1,x2])
        xArr.append(i)
        yArr.append(j)
        i = i+1
        j = j+1
    distance_temp = deepcopy(distance)
    while (len(primTour)!=len(distance_temp)):
        dis = min(distance)
        disIndex = distance.index(dis)
        x0 = xArr[disIndex]
        primTour.append(x0)
        distance.pop(disIndex)
        xArr.pop(disIndex)
    city = len(primTour)
    tl = tour_length(cm, primTour,city)
    return tl
    
##Calculates the nearest distance from an unvisited city to the start city.
def partC(unexplored, source,cm):
    start = source
    dis = 0
    unexp = deepcopy(unexplored)
    for u in unexp:
        d = cm[start,u]
        dis = dis + d
##    print d

    return dis

##Sums up a, b and c to give us the h heuristic
def computeH(source,start,current,unexplored, explored, index, totalIndices,CITIES,cm):
    dis = []
    indices = []
    ind, a = partA(unexplored, explored, current,cm)
    b = partB(unexplored, current,index,cm,explored)
    c = partC(unexplored, source,cm)
    dis.append(c)
    indices.append(current)
    h = a+ b+ c
    return h,dis,indices

##Special case to decide the start city of the TSP
def passZero(unexplored, cm, totalIndices, index):
    g = 0
    exp = []
    unvisited = deepcopy(unexplored)
    fArr = []
    xArr = []
    yArr = []
    aIndex = []
    
    for v in unexplored:
        nodeIn = unvisited.index(v)
        unvisited.pop(nodeIn)
        exp.append(v)
        aIndex,h1 = partA(unvisited, exp, v,cm)

        h2 = partB(unvisited, v, index, cm, exp)
        h3 = partC(unvisited,v,cm)
        h = h1 + h2 + h3
        f = g + h
        fArr.append(f)
        yArr.append(v)
        xArr.append(-1)
        unvisited = deepcopy(unexplored)
    fMin = min(fArr)
    fMinIndex = fArr.index(fMin)
    return fMinIndex,fArr,xArr,yArr
    
def main_run():
    
    explored = []
    visited = []
    unexplored = []
    totalIndices = []
    totalDM = []
    coords = []
    dis = []
    disInd = []
    x = []
    y = []
    x1 = []
    y1 = []
    fFunc = []
    index = []
    start = 0
    cost = 0
    flag = 0
    source = 0
    fMinInd = 0
    xMin = 0
    yMin = 0
    unexp= []
    fStart = []
    xStart = []
    yStart = []
    cm = []
    fFunc = []
    x1 = []
    y1 = []
    fEx = []
    exp = []
    f1 = open(sys.argv[1],"r")

    content = f1.readlines()
    for line in content:
        if line.startswith(" "):
            line = line[1:]
        if line[0].isdigit():
            col = line.split()
            index.append(col[0])
            x.append(col[1])
            y.append(col[2])
##Coords store the coordinates of all the points in the dataset. These coordinates are sent to the cartesian matrix function to calculate the distance matrix using euclidean distance
        coords = np.array(zip(x,y), dtype=[('x',float),('y',float)])
    for j in range(0,len(index)):
        if x[j].startswith("-") or y[j].startswith("-"):
            x[j] = abs(int(x[j]))
            y[j] = abs(int(y[j]))
        x[j] = float(x[j])
        y[j] = float(y[j])
    city = len(coords)
    cm = cartesian_matrix(coords)
    for i in range(0, len(index)):
        totalIndices.append(i)
        unexplored.append(i)

    start, fStart, xStart, yStart = passZero(unexplored, cm, totalIndices, index)

    unex = deepcopy(unexplored)
##Adding start node to the explored list and removing startb node from unexplored list
    for unex in unexplored:
        if start == unex:
            startIn = totalIndices.index(unex)
            unexplored.pop(startIn)
            explored.append(start)

    source = start
    visited = []
    temp = []
    fFunc1 = []
    while flag == 0:
##Priority queue keeps track of the f values and nodes traversed to and from to get the f value
        pq = q.PriorityQueue()

        tempFlag = 0
        fFunc = []
        x1 = []
        y1 = []
##        visited = []
        eI = 0
        temp_flag = 0
        if len(explored) == len(index):
            flag = 1
            break
##Loop computes f values for all cities explored and all unexplored cities
        for ex in explored:
            for unex in unexplored:
                k = []
                current = unex
                g = computeG(explored, current, cm)
                h,dis,disInd = computeH(source,start,current,unexplored, explored, index, totalIndices, city,cm)
                f = g + h
                fFunc.append(f)
                x1.append(ex)
                y1.append(unex)
                k.append(ex)
                k.append(unex)

                pq.put((f, k))
## Getting nodes with minimum f value from Priority Queue       
        fMin,visited = pq.get()
        fFunc1.append(fMin)

##        explored = temp
        lastNode = explored[0]
        toPop = explored[-1]

        for ele in visited:
            if not ele in explored:
                k = ele
##If there is only one node i.e the start node in the explored list, next node is appended to it. 
        if len(explored) == 1:
            explored = visited
            for ele in explored:
                if ele in unexplored:
                    eleIn = unexplored.index(ele)
                    unexplored.pop(eleIn)
##If there are more than one nodes in the lexplored list, we compare the new f value and coordinates obtained from Priority queue to the ones in the explored array and previous f.
##If new f is lower than previous f, we compare the new nodes to the ones in the array. If the start node of new value is not the last value of the explored list, we trace to find the new value in the list and replace all nodes from that node
        if len(explored) > 1:
            if visited[0] in explored:
                if visited[0] == explored[-1]:
                    visitSec = visited[1]
                    explored.append(visitSec)
                    if visitSec in unexplored:
                        visitSecInd = unexplored.index(visitSec)
                        unexplored.pop(visitSecInd)
                else:
                    if fMin < fFunc1[-1]:
                        k = visited[1]
                        l = explored.index(visited[0])
                        for x in range(l+1, len(explored)):
                            temp_exp = explored[x]
                            unexplored.append(temp_exp)
                            unexplored.sort()
                            explored.pop(explored.index(temp_exp))
                            explored.append(k)
                        if visited[1] in unexplored:
                            m = unexplored.index(k)
                            unexplored.pop(m)
                        temp_exp = explored[x]
                        unexplored.append(temp_exp)
                        unexplored.sort()
                        explored.pop(explored.index(temp_exp))
                        explored.append(k)
                        if visited[1] in unexplored:
                            m = unexplored.index(k)
                    else:
                        k = visited[1]
                        if not k in explored:
                            explored.append(k)
                        if k in unexplored:
                            unexplored.pop(unexplored.index(k))
                            unexplored.sort()            
            else:
                k = visited[1]
                if not k in explored:
                    explored.append(k)
                if k in unexplored:
                    unexplored.pop(unexplored.index(k))
                    unexplored.sort()
##If unexplored list is empty, we terminate the loop. This means all nodes have been traversed
        if not unexplored:
            flag = 1

##We append the start node to the tour and calculate tour length      
    city = len(coords)+1
    explored.append(source)
    tl = tour_length(cm, explored,city)
    print("Time taken:%s seconds" % (time.time() - start_time))
    print ("Tour length of A star is:{}".format(tl))


if __name__ == "__main__":
   main_run()
