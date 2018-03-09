try:
   from pyevolve import G1DList, GAllele
except:
   ImportError
try:
   from pyevolve import GSimpleGA
except:
   ImportError
try:
   from pyevolve import Mutators
except:
   ImportError
try:
   from pyevolve import Crossovers
except:
   ImportError
try:
   from pyevolve import Consts
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
   import numpy as np
except:
   ImportError
try:
   import sys, random
except:
   ImportError
random.seed(1024)
try:
   from math import sqrt
except:
   ImportError
PIL_SUPPORT = None

try:
   from PIL import Image, ImageFont, ImageDraw
   PIL_SUPPORT = True
except:
   PIL_SUPPORT = False


coords = []
WIDTH   = 1024
HEIGHT  = 768
LAST_SCORE = -1
visited = []
xx = []

tl = []
##Cartesian matrix creates distance matrix
def cartesian_matrix(coords):
   """ A distance matrix """
   matrix={}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist=sqrt(dx*dx + dy*dy)
         matrix[i,j] = dist
   return matrix

##Function computes length of our entire tour
def tour_length(matrix, tour,CITIES):
   """ Returns the total length of the tour """
   total = 0
   t = tour.getInternalList()
   for i in range(CITIES):
      j      = (i+1)%CITIES
      total += matrix[t[i], t[j]]
   return total

def tour_length1(matrix, tour,CITIES):
   """ Returns the total length of the tour """
   total = 0
   t = tour
   for i in range(CITIES):
      j      = (i+1)%CITIES
      total += matrix[t[i], t[j]]
   return total
##Function writes tour to png file
def write_tour_to_img(coords, tour):

   num_cities=len(tour)
   for i in range(num_cities):
      j=(i+1)%num_cities
      city_i=tour[i]
      city_j=tour[j]
      x1,y1=coords[city_i]
      x2,y2=coords[city_j]
      xx.append(city_j)

   for x,y in coords:
      x,y=int(x),int(y)
   return xx

def G1DListTSPInitializator(genome, **args):
   """ The initializator for the TSP """
   lst = [i for i in xrange(genome.getListSize())]
   random.shuffle(lst)
   genome.setInternalList(lst)

def main_run():

   table = {}
   index = []
   x = []
   y = []
   cm     = []
   global xx, coords, WIDTH, HEIGHT

   opfile = "output_tsp.txt"

   f1 = open(sys.argv[1],"r")
   content = f1.readlines()
   print("==================File Name {}===================".format(sys.argv[1]))
   for line in content:
      if line.startswith(" "):
         line = line[1:]
         
      if line[0].isdigit():
         col = line.split()
         index.append(col[0])
         x.append(col[1])
         y.append(col[2])
   table["Index"] = index
   table["x"] = x
   table["y"] = y
   coords = np.array(zip(x,y), dtype=[('x',float),('y',float)])


   for j in range(0,len(index)):
      if x[j].startswith("-") or y[j].startswith("-"):
         x[j] = abs(int(x[j]))
         y[j] = abs(int(y[j]))
      x[j] = float(x[j])
      y[j] = float(y[j])

   CITIES = len(coords)

   cm     = cartesian_matrix(coords)
   genome = G1DList.G1DList(len(coords))
   cm1     = cartesian_matrix(coords)


   genome.evaluator.set(lambda chromosome: tour_length(cm1, chromosome,CITIES))
   genome.crossover.set(Crossovers.G1DListCrossoverEdge)
   genome.initializator.set(G1DListTSPInitializator)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(1000)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.02)
   ga.setPopulationSize(80)

   ga.evolve(freq_stats=0)
   best = ga.bestIndividual()

   xx = write_tour_to_img(coords, best)

   if sys.argv[1]=="att48.tsp":
    o = open (opfile, "w+")
    o.write ("TOUR_SECTION\n")
    for k in range(0,CITIES):
        o.write ("{}\n".format(best[k]))
    o.close()
   tl = tour_length1(cm, xx,CITIES)
   time = ga.printTimeElapsed()


   print("Genetic Algorithm - The tour length for file {} is:{} and time taken is:{}".format(sys.argv[1],tl,time))


    

if __name__ == "__main__":
   main_run()
