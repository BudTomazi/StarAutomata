# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:28:35 2021

@author: budto
"""

from PIL import Image
import random as r
import numpy as np

IMAGE_SIZE = 30
FRAMES = 25
PARTICLES = 1800

COLORS = [255,(255<<8),(255<<16),(255<<8)+255,(255<<16)+255,(255<<16)+(255<<8),(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255]

class Part:
    
    def __init__(self, weight, d):
        self.weight = weight
        self.d = d

def update(world):
    new_world = [[0 for i in range(IMAGE_SIZE)] for j in range(IMAGE_SIZE) ]
    for w1 in range(len(world)):
        for w2 in range(len(world[0])):
            if(world[w1][w2] != 0):
                sumvec = world[w1][w2].d * world[w1][w2].weight
                for i in range(3):
                    for j in range(3):
                        if(w1+i-1 in range(IMAGE_SIZE) and w2+j-1 in range(IMAGE_SIZE)):
                            if(world[w1+i-1][w2+j-1] != 0 and not(i == 1 and j == 1)):
                                sumvec += world[w1+i-1][w2+j-1].weight * np.array([i-1,j-1])
                # print(sumvec)
                if(sumvec[0] != 0):
                    sumvec[0] /= abs(sumvec[0])
                if(sumvec[1] != 0):
                    sumvec[1] /= abs(sumvec[1])
                if(w1 + sumvec[0] in range(IMAGE_SIZE) and w2 + sumvec[1] in range(IMAGE_SIZE)):
                    if new_world[w1 + sumvec[0]][w2 + sumvec[1]] == 0:
                        new_world[w1 + sumvec[0]][w2 + sumvec[1]] = Part(world[w1][w2].weight,sumvec)
                    else:
                        new_world[w1 + sumvec[0]][w2 + sumvec[1]].d += sumvec
                        if(new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[0] != 0):
                            new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[0] /= abs(new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[0])
                        if(new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[1] != 0):
                            new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[1] /= abs(new_world[w1 + sumvec[0]][w2 + sumvec[1]].d[1])
                        new_world[w1 + sumvec[0]][w2 + sumvec[1]].weight += world[w1][w2].weight
    return new_world

def p_world(world):
    new_world = [[0 for i in range(IMAGE_SIZE)] for j in range(IMAGE_SIZE) ]
    for w in range(len(world)):
        for t in range(len(world[w])):
            if(world[w][t] != 0):
                new_world[w][t] = world[w][t].weight
    for w in new_world:
        print(w)
    print("-------------")
                

def to_image(world, num):
    new_world = []
    for w in range(len(world)):
        for t in range(len(world[w])):
            if(world[w][t] != 0):
                new_world.append(COLORS[min(world[w][t].weight-1,10)])
            else:
                new_world.append(0)
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
    img.putdata(new_world)
    img.save('images2/image' + str(num) + '.png')

world = [[0 for i in range(IMAGE_SIZE)] for j in range(IMAGE_SIZE) ]
# world = [([0]*IMAGE_SIZE)] * IMAGE_SIZE
# world = np.array((IMAGE_SIZE,IMAGE_SIZE))
vecs = [np.array([1,0]),np.array([1,1]),np.array([0,1]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1]),np.array([0,-1]),np.array([1,-1])]

parts = []
for i in range(PARTICLES):
    a = r.randint(0,7)
    parts.append(Part(1, vecs[a]))

for i in range(PARTICLES):
    # world[i%3+1][i//3+1] = parts[i]
    world[r.randint(0, IMAGE_SIZE-1)][r.randint(0, IMAGE_SIZE-1)] = parts[i]
# world[3][3] = Part(1,np.array([-1,-1]))
# world[0][0] = Part(3,np.array([1,1]))

# world[0][2] = Part(1,np.array([1,0]))
# world[2][3] = Part(1,np.array([-1,0]))

for i in range(FRAMES):
    to_image(world,i)
    world = update(world)

# to_image(world)
# # p_world(world)
# world = update(world)
# # p_world(world)
# world = update(world)
# # p_world(world)
# world = update(world)
# # p_world(world)
# world = update(world)
# # p_world(world)
# world = update(world)
# p_world(world)