# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:28:35 2021

@author: budto
"""

from PIL import Image
import random as r
import numpy as np

IMAGE_SIZE = 50
FRAMES = 200
PARTICLES = 900
GRAV_RADIUS = 7
RANDOM_BURSTS = True
VELOCITY_BURSTS = True
NEGATIVE_MASS = True

VECTORS = [np.array([1,0]),np.array([1,1]),np.array([0,1]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1]),np.array([0,-1]),np.array([1,-1])]
DIAGONAL = [np.array([1,1]),np.array([1,-1]),np.array([-1,1]),np.array([-1,-1])]
COLORS = [255,(255<<8),(255<<16),(255<<8)+255,(255<<16)+255,(255<<16)+(255<<8),(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255,(255<<16)+(255<<8)+255]

class Part:
    def __init__(self, weight, d):
        self.weight = weight
        self.d = d

def update(world):
    counts = 0
    new_world = [[0 for i in range(IMAGE_SIZE)] for j in range(IMAGE_SIZE) ]
    for w1 in range(len(world)):
        for w2 in range(len(world[0])):
            if(world[w1][w2] != 0 and world[w1][w2].weight != 0):
                if(abs(world[w1][w2].weight) < 6 or r.randint(0, abs(world[w1][w2].weight) - 6) == 0):# or r.randint(0, world[w1][w2].weight - 6) == 0):
                    #sum forces on object with velocity
                    sumvec = world[w1][w2].d * abs(world[w1][w2].weight)
                    sign = world[w1][w2].weight / abs(world[w1][w2].weight)
                    for i in range(1+2*GRAV_RADIUS):
                        for j in range(1+2*GRAV_RADIUS):
                            if(world[(w1+i-GRAV_RADIUS)%IMAGE_SIZE][(w2+j-GRAV_RADIUS)%IMAGE_SIZE] != 0 and not(i == 1 and j == 1)):
                                sumvec += int(sign) * (world[(w1+i-GRAV_RADIUS)%IMAGE_SIZE][(w2+j-GRAV_RADIUS)%IMAGE_SIZE].weight * np.array([i-GRAV_RADIUS,j-GRAV_RADIUS])) // max(abs(max(abs(i-GRAV_RADIUS),abs(j-GRAV_RADIUS))),1)
                    #normalize motion vector
                    if(sumvec[0] != 0):
                        sumvec[0] /= abs(sumvec[0])
                    if(sumvec[1] != 0):
                        sumvec[1] /= abs(sumvec[1])
                    
                    #check if need to combine
                    index_0 = (w1 + sumvec[0])%IMAGE_SIZE
                    index_1 = (w2 + sumvec[1])%IMAGE_SIZE
                    if new_world[index_0][index_1] == 0:#empty case
                        new_world[index_0][index_1] = Part(world[w1][w2].weight,sumvec)
                    else:#combine case
                        new_world[index_0][index_1].d += sumvec
                        if(new_world[index_0][index_1].d[0] != 0):
                            new_world[index_0][index_1].d[0] /= abs(new_world[index_0][index_1].d[0])
                        if(new_world[index_0][index_1].d[1] != 0):
                            new_world[index_0][index_1].d[1] /= abs(new_world[index_0][index_1].d[1])
                        new_world[index_0][index_1].weight += world[w1][w2].weight
                else:
                    DIAGONAL = [np.array([1,1]),np.array([1,-1]),np.array([-1,1]),np.array([-1,-1])]
                    VECTORS = [np.array([1,0]),np.array([1,1]),np.array([0,1]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1]),np.array([0,-1]),np.array([1,-1])]
                    RANDOM = []
                    for i in range(4):
                        RANDOM.append(VECTORS.pop(r.randint(0,len(VECTORS)-1)))
                    counts+=1
                    w = world[w1][w2].weight
                    d =  world[w1][w2].d
                    weights = [0,0,0,0]
                    weights[0] = w//2
                    weights[1] = w - weights[0]
                    weights[0], weights[2] = weights[0]//2, weights[0] - weights[0]//2
                    weights[1], weights[3] = weights[1]//2, weights[1] - weights[1]//2
                    BURST_RULE = []
                    if(RANDOM_BURSTS):
                        BURST_RULE = RANDOM
                    else:
                        BURST_RULE = DIAGONAL
                    for v in range(len(BURST_RULE)):
                        #check if need to combine
                        if(VELOCITY_BURSTS):
                            index_0 = (w1 + BURST_RULE[v][0] + d[0])%IMAGE_SIZE
                            index_1 = (w2 + BURST_RULE[v][1] + d[1])%IMAGE_SIZE
                        else:
                            index_0 = (w1 + BURST_RULE[v][0])%IMAGE_SIZE
                            index_1 = (w2 + BURST_RULE[v][1])%IMAGE_SIZE
                        if new_world[index_0][index_1] == 0:#empty case
                            new_world[index_0][index_1] = Part(weights[v],BURST_RULE[v])
                        else:#combine case
                            new_world[index_0][index_1].d += BURST_RULE[v]
                            if(new_world[index_0][index_1].d[0] != 0):
                                new_world[index_0][index_1].d[0] /= abs(new_world[index_0][index_1].d[0])
                            if(new_world[index_0][index_1].d[1] != 0):
                                new_world[index_0][index_1].d[1] /= abs(new_world[index_0][index_1].d[1])
                            new_world[index_0][index_1].weight += weights[v]
    print(counts)
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
                if world[w][t].weight < 0:     
                    new_world.append(COLORS[min(abs(world[w][t].weight)-1,10)] >> 1)
                else:
                    new_world.append(COLORS[min(abs(world[w][t].weight)-1,10)])                    
            else:
                new_world.append(0)
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
    img.putdata(new_world)
    img.save('images2/image' + str(num) + '.png',resample=None)
    
def sum_weights(world):
    total =[]
    for w in world:
        for t in w:
            if(t!=0):
                total.append(t.weight)
    return total

world = [[0 for i in range(IMAGE_SIZE)] for j in range(IMAGE_SIZE)]
vecs = [np.array([1,0]),np.array([1,1]),np.array([0,1]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1]),np.array([0,-1]),np.array([1,-1])]

parts = []
for i in range(PARTICLES):
    a = r.randint(0,7)
    parts.append(Part(r.randint(0,1)*2 -1, vecs[a]))

for i in range(PARTICLES):
    # world[i%3+1][i//3+1] = parts[i]
    world[r.randint(0, IMAGE_SIZE-1)][r.randint(0, IMAGE_SIZE-1)] = parts[i]
# world[40][40] = Part(1800, np.array([1,1]))
# world[10][10] = Part(-1800, np.array([1,1]))
# world[0][0] = Part(-4,np.array([1,1]))
# world[3][3] = Part(4,np.array([-1,-1]))

for i in range(FRAMES):
    # print(sum_weights(world))
    to_image(world,i)
    world = update(world)

