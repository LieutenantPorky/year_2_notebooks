import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import json
import copy


map = mpimg.imread("map.png")
# List of 30 US state capitals and corresponding coordinates on the map

with open('capitals.json', 'r') as capitals_file:
    capitals = json.load(capitals_file)


capitals_list = list(capitals.items())

capitals_list = [(c[0], tuple(c[1])) for c in capitals_list]
def coord(path):
        """Strip the city name from each element of the path list and return
        a list of tuples containing only pairs of xy coordinates for the
        cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        _, coord = path
        return coord

def coords(path):
        """Strip the city name from each element of the path list and return
        a list of tuples containing only pairs of xy coordinates for the
        cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        _, coords = zip(*path)
        return coords

def show_path(path_, starting_city, w=35, h=15):
    """Plot a TSP path overlaid on a map of the US States & their capitals."""
    path=coords(path_)
    x, y = list(zip(*path))

    _, (x0, y0) = starting_city

    plt.imshow(map)
    plt.plot(x0, y0, 'y*', markersize=15)  # y* = yellow star for starting point
    plt.plot(x + x[:1], y + y[:1])  # include the starting point at the end of path
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])

def temp(t, a = .95, t_0 = 1e8):
    return (a ** t) * t_0
def getPath(n=8):

    test_cities = []
    mod_capitals = list(capitals_list)

    for i in range(0,n):
        test_cities.append(mod_capitals.pop(np.random.randint(len(mod_capitals))))

    return test_cities

def exchange(path):
    #choose two random points, and reverse the path between them - exclude the first and last item though, to avoid
    #problems with thr path not being cyclic anymore

    a = 1 + np.random.randint(len(path) - 2)
    b = a + np.random.randint(1, len(path) - a)

    a = 1 + np.random.randint(len(path)-2)
    b = a + np.random.randint(1, len(path) - a)
    return path[:a] + path[b:a-1:-1] + path [b+1:]

def getLength(path):
    total = 0
    cPath = [i for i in coords(path)]
    cPath.append(coord(path[0]))

    for i in range(len(cPath) - 1):
        total += np.sum((np.array([j for j in cPath[i]]) - np.array([j for j in cPath[i+1]]))**2) ** 0.5

    return total


def optimize(initialPath, tStep=200, alpha=0.97,T=1000):
    distances = [getLength(initialPath)]
    paths = [initialPath]
    for t in np.arange(tStep):
        newPath = exchange(list(initialPath))

        oldD = getLength(initialPath)
        newD = getLength(newPath)

        if np.exp((oldD - newD)/temp(t,alpha,T)) > np.random.random():
            initialPath = newPath

        distances.append(newD)
        paths.append(newPath)

    return paths, distances

def solvePath(path,iterN=20,alpha=0.95,T=1000):
    currentPath = [path]
    dist = getLength(path)
    for i in range(iterN):
        #print(dist)
        newPath, newDist = optimize(path, 1250,alpha=alpha, T=T)
        lowestIndex = np.argmin(newDist[-200:])

        if newDist[lowestIndex] < dist:
            currentPath = newPath[-200:][lowestIndex]
            dist = newDist[-200:][lowestIndex]

    return currentPath, dist


new = [("Bismark", (356.2,151.7)),("Helena", (218.3,140.6)),("Santa Fe", (272.4,344)),("Augusta", (742.5,151.6)),("Carson City", (93,248.4))]

truePath = getPath(len(capitals_list))
truePath.extend(new)

f=open("paths.txt",'w')
path, dist = solvePath(list(truePath),iterN=1,T=500)
while True:
    newpath, newdist = solvePath(list(truePath),iterN=1,T=500)
    if newdist < dist:
        path = newpath
        dist = newdist
        print("lowest path is:{0},\n with length {1} \n\n\n".format(path, dist))
        f.write(str(path) + ", " + str(dist))
