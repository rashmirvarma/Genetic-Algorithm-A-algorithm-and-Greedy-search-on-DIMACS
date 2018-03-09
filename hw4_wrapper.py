import os
import csv
import sys
from os import system


def main_run():

    flag = 1
    path1 = sys.argv[1]
    for files in os.listdir(path1):
        path2 = os.path.join(path1,files)

        if not files.startswith('.'):
            with open(path2) as f1:
##                content = f1.readlines()
##                for line in content:
##                    if line.startswith(" "):
##                     line = line[1:]
##                    if line == "EDGE_WEIGHT_TYPE : EUC_2D":
                        system("python hw4_greedy.py {}".format(path2))
                        system("python pyevolve_ex12_tsp.py {}".format(path2))


if __name__ == "__main__":
   main_run()
