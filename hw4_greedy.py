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
   import sys
except:
   ImportError
try:
   import numpy as np
except:
   ImportError
try:
   import time
except:
   ImportError
try:
   import collections
except:
   ImportError

start_time = time.time()
##Creates the distance matrix
def cartesian_matrix(coords):
   """ A distance matrix """
   matrix={}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist=sqrt(dx*dx + dy*dy)
         matrix[i,j] = dist
   return matrix
##Computes tour length
def tour_length(matrix, tour,CITIES):
   """ Returns the total length of the tour """
   total = 0
   t = tour
   for i in range(CITIES):
      j      = (i+1)%CITIES
      total += matrix[t[i], t[j]]
   return total
##Returns index of duplicates
def list_duplicates_of(seq,item):
   return [i for i, v in enumerate(seq) if v == item]

def main_run():
   start = 0
   index = []
   x = []
   y = []
   cm     = []
   visited = []
   temp = []
   temp1 = []
   temp2 = []
   coords = {}
   miny = 0
   p = []
   flag = 0
   dset = []

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

      listDu = []
      coords = np.array(zip(x,y), dtype=[('x',float),('y',float)])

   CITIES = len(coords)

   cm     = cartesian_matrix(coords)
##    print cm
   for pInd in range(0, len(index)):
      p.append(pInd)
   visited.append(start)
   for everyP in p:
      if start == everyP:
         indexP = p.index(everyP)
         p.pop(indexP)

   i = start
   mini=0

   while(flag == 0):
      if not p:
         flag = 1
         break
      temp = []
      temp1 = []
      for m in range(0,len(index)):
         temp1.append(cm[i,m])
      for j in p:
         temp.append(cm[i,j])
  
      mini = min(temp)

      miny = temp1.index(mini)
      for l in visited:
         if miny == l:
            for i in range(0, len(temp1)):
               if mini == temp1[i]:
                  if i in visited:
                     continue
                  else:
                     visited.append(i)
                     miny = i
                     break

      if not miny in visited:
         visited.append(miny)
         
           


      temp2.append((i,miny))
      i = miny
      if p:
         for ele in p:
            if miny == ele:
               tempInd = p.index(ele)
               p.pop(tempInd)

      
   visited.append(start)
   x1 = miny
   temp2.append((x1,start))
   tl = tour_length(cm, visited,CITIES)

   print ("Greedy Algorithm - Tour length for {} is: {}".format(sys.argv[1],tl))
   print("Time taken:%s seconds" % (time.time() - start_time))

      
         
   

         


if __name__ == "__main__":
   main_run()
